import pandas as pd
import numpy as np
import keras
import keras_tuner as kt
from sklearn.preprocessing import StandardScaler
import joblib
from pathlib import Path
import matplotlib.pyplot as plt

import matplotlib
matplotlib.use("TkAgg")

base_folder = Path("/media/faraaz/Data_faru_lnx/College/MSc/Project/exfor/Neural_Network/models")
base_folder.mkdir(parents=True, exist_ok=True)
csv_file = Path("/media/faraaz/Data_faru_lnx/College/MSc/Project/exfor/exfor_files/lanthanide_exfor_ldegsm_gdrsmlo.csv")

df = pd.read_csv(csv_file)
target_column = "Cross_Section_mb"

cols_to_scale = ["Energy_MeV", "Z1", "N1", "Z2", "N2", "Er1", "Wr1", "S1", "CSp1", "Qn", "Shell", "a_exp"]

Z, N = 62, 87
ZN_mask = (df["Z1"] == Z) & (df["N1"] == N)

feature_cols = cols_to_scale + ["beta2"]

#transform  training and test data with standard scaler z scaling
feature_scaler = StandardScaler().fit(df.loc[~ZN_mask, cols_to_scale])
Xtrain = df.loc[~ZN_mask, feature_cols].copy()
Xtrain[cols_to_scale] = feature_scaler.transform(df.loc[~ZN_mask, cols_to_scale])
Xtest = df.loc[ZN_mask, feature_cols].copy()
Xtest[cols_to_scale] = feature_scaler.transform(df.loc[ZN_mask, cols_to_scale])

yraw = df[target_column]
ytrain = yraw[~ZN_mask]
ytest = yraw[ZN_mask]

# log scaling used to reduce cross section values similar to other inputs
y_train = ytrain.values.reshape(-1, 1)
y_train = np.log1p(y_train)
y_test = ytest.values.reshape(-1, 1)
y_test = np.log1p(y_test)
target_scaler = StandardScaler()
ytrain = target_scaler.fit_transform(y_train)   
ytest = target_scaler.transform(y_test)   

#save standard scalers
joblib.dump(feature_scaler, base_folder / "feature_scaler_19Sep.pkl")
joblib.dump(target_scaler, base_folder / "target_scaler_19Sep.pkl")


def build_model(hp):
    model = keras.Sequential()
    model.add(keras.layers.InputLayer(input_shape=(Xtrain.shape[1],)))

    # Test on number on neurons and activation functions
    for i in range(hp.Int("num_layers", 2, 5)):
        model.add(keras.layers.Dense(
            units=hp.Int(f"units_{i}", min_value=64, max_value=256, step=64),
            activation=hp.Choice(f"activation_{i}", ["relu", "elu", "swish"])
        ))

        # Try Dropout
        if hp.Boolean(f"dropout_{i}"):
            model.add(keras.layers.Dropout(rate=hp.Float(f"drop_rate_{i}", 0.1, 0.3, step=0.1)))

    # Output layer-Linear prevents negative values
    model.add(keras.layers.Dense(1, activation="linear"))

    # Sample learning rate
    lr = hp.Float("learning_rate", 1e-4, 1e-2, sampling="log")

    model.compile(
        optimizer=keras.optimizers.Adam(learning_rate=lr),
        loss="mse",
        metrics=["mae"]
    )
    return model

tuner = kt.BayesianOptimization(
    build_model,
    objective="loss",
    max_trials=15,
    directory=base_folder,
    project_name="cross_section_tuning",
    overwrite=True
)

#early stopping for faster computation
early_stopping = keras.callbacks.EarlyStopping(
    monitor="loss", patience=10, restore_best_weights=True
)

print("Starting KerasTuner Search...")
tuner.search(
    Xtrain, ytrain,
    epochs=100,
    callbacks=[early_stopping],
    verbose=1
)

# Save the best model
best_model = tuner.get_best_models(num_models=1)[0]
final_model_path = base_folder / "gnModel_Final_Optimized.keras"
best_model.save(final_model_path)
print(f"\nOptimization complete! Best model saved to: {final_model_path}")

#--------------------------------------------------------------------------------------------------
#Predict on test data
y_pred_scaled = best_model.predict(Xtest)

# Flatten and transform the predictions
y_pred_log = target_scaler.inverse_transform(y_pred_scaled)
y_pred_unscaled = np.expm1(y_pred_log).flatten()

y_test_log = target_scaler.inverse_transform(ytest)
y_test_unscaled = np.expm1(y_test_log).flatten()

#-----------------------------------------------------------------------------------------------------------
#Plotting

energy_test = df.loc[ZN_mask, "Energy_MeV"].values
y_true_exfor = df.loc[ZN_mask, target_column].values  

order = np.argsort(energy_test)
energy_sorted = energy_test[order]
y_true_sorted = y_true_exfor[order]
y_pred_sorted = y_pred_unscaled[order]


result = {"Energy_MeV" : energy_test,
          "NN_cs": y_pred_sorted,
          "exfor_cs": y_true_exfor
          }
result_df = pd.DataFrame(result)
result_df.to_excel(base_folder / "Sm149ld_egsm.xlsx")

plt.figure(figsize=(8, 6))
plt.plot(energy_sorted, y_true_sorted, "o-", color="black", label="EXFOR (measured)", markersize=4)
plt.plot(energy_sorted, y_pred_sorted, "o-", color="dodgerblue", label="Predicted", markersize=4, alpha=0.7)
plt.xlabel("Energy (MeV)")
plt.ylabel("Cross Section (mb)")
plt.title(f"isotope Z={Z}, N={N}: EXFOR vs Predicted")
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()