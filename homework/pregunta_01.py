# pylint: disable=line-too-long
"""
Escriba el codigo que ejecute la accion solicitada.
"""
import matplotlib
matplotlib.use("Agg")  # Fuerza backend no interactivo

import matplotlib.pyplot as plt
import pandas as pd
import os
"""
Escriba el codigo que ejecute la accion solicitada.
"""


def pregunta_01():
    """
    Genera un dashboard estático con gráficos sobre los envíos de productos.
    """
    # Crear la carpeta "docs" si no existe
    os.makedirs("docs", exist_ok=True)

    # Cargar datos con manejo de errores
    try:
        df = pd.read_csv("files/input/shipping-data.csv")
    except FileNotFoundError:
        print("Error: No se encontró el archivo 'files/input/shipping-data.csv'")
        return

    # Gráfico de envíos por Warehouse
    plt.figure()
    counts = df["Warehouse_block"].value_counts()
    counts.plot.bar(
        title="Shipping per Warehouse",
        xlabel="Warehouse block",
        ylabel="Record count",
        color="tab:blue",
        fontsize=8
    )
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.savefig("docs/shipping_per_warehouse.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Gráfico de modo de envío
    plt.figure()
    counts = df["Mode_of_Shipment"].value_counts()
    colors = plt.cm.tab10.colors[:len(counts)]  # Asignar colores dinámicamente
    counts.plot.pie(
        title="Mode of shipment",
        wedgeprops=dict(width=0.35),
        ylabel="",
        colors=colors,
    )
    plt.savefig("docs/mode_of_shipment.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Gráfico de calificación del cliente
    plt.figure()
    df_rating = df.groupby("Mode_of_Shipment")["Customer_rating"].describe()[["mean", "min", "max"]]

    plt.barh(
        y=df_rating.index.values,
        width=df_rating["max"].values - 1,
        left=df_rating["min"].values,
        height=0.9,
        color="lightgray",
        alpha=0.8,
    )   

    colors = ["tab:green" if value >= 3.0 else "tab:orange" for value in df_rating["mean"].values]

    plt.barh(
        y=df_rating.index.values,
        width=df_rating["mean"].values - 1,
        left=df_rating["min"].values,
        height=0.5,
        color=colors,
        alpha=1.0,
    )

    plt.title("Average Customer Rating")
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.gca().spines["left"].set_visible(False)
    plt.gca().spines["bottom"].set_visible(False)
    plt.savefig("docs/average_customer_rating.png", dpi=300, bbox_inches="tight")
    plt.close()

    # Distribución del peso de los envíos
    plt.figure()
    df["Weight_in_gms"].plot.hist(
        title="Shipping weight distribution",
        color="tab:orange",
        edgecolor="white",
        bins=20  
    )
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.savefig("docs/weight_distribution.png", dpi=300, bbox_inches="tight")
    plt.close()

    print(" Dashboard generado en la carpeta 'docs'")

if __name__ == "__main__":
    pregunta_01()
