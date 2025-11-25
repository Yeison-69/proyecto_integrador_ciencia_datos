import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def graficar_importancia_variables(modelo, X_train):
    """
    Genera un gráfico de importancia de variables
    para modelos basados en árboles como RandomForest.
    """

    importancias = modelo.feature_importances_
    variables = X_train.columns

    df_importancias = pd.DataFrame({
        "Variable": variables,
        "Importancia": importancias
    }).sort_values(by="Importancia", ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(data=df_importancias, x="Importancia", y="Variable", palette="viridis")
    plt.title("Importancia de las Variables")
    plt.xlabel("Importancia")
    plt.ylabel("Variable")
    plt.tight_layout()
    plt.show()

    return df_importancias
