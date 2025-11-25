import matplotlib.pyplot as plt
import seaborn as sns

def grafico_premios_por_ciudad(df):
    plt.figure(figsize=(8,4))
    sns.barplot(x="ciudad", y="premio_mayor_millones", data=df, estimator="mean")
    plt.xticks(rotation=45)
    plt.title("Promedio de premios por ciudad")
    return plt

def grafico_premios_en_el_tiempo(df):
    plt.figure(figsize=(10,4))
    sns.lineplot(x="fecha", y="premio_mayor_millones", data=df)
    plt.title("Premios a lo largo del tiempo")
    return plt
