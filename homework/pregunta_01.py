import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")  # Forzar backend no interactivo
import pandas as pd
import os

def pregunta_01():
    """
    El archivo `files//shipping-data.csv` contiene información sobre los envíos
    de productos de una empresa. Cree un dashboard estático en HTML que
    permita visualizar los siguientes campos:

    * `Warehouse_block`
    * `Mode_of_Shipment`
    * `Customer_rating`
    * `Weight_in_gms`
    
    El dashboard generado debe ser similar a este:
    https://github.com/jdvelasq/LAB_matplotlib_dashboard/blob/main/shipping-dashboard-example.png
    
    Tenga en cuenta los siguientes cambios respecto al video:
    * El archivo de datos se encuentra en la carpeta `data`.
    * Todos los archivos deben ser creados en la carpeta `docs`.
    * Su código debe crear la carpeta `docs` si no existe.
    """
    # Crear la carpeta 'docs' si no existe
    os.makedirs("docs", exist_ok=True)
    
    # Leer los datos
    df = pd.read_csv("files/input/shipping-data.csv")
    
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
    plt.savefig("docs/shipping_per_warehouse.png")
    
    # Gráfico de modo de envío
    plt.figure()
    counts = df["Mode_of_Shipment"].value_counts()
    counts.plot.pie(
        title="Mode of shipment",
        wedgeprops=dict(width=0.35),
        ylabel="",
        colors=["tab:blue", "tab:orange", "tab:green"],
    )
    plt.savefig("docs/mode_of_shipment.png")
    
    # Gráfico de calificación del cliente
    plt.figure()
    df_rating = (df[["Mode_of_Shipment", "Customer_rating"]].groupby("Mode_of_Shipment").describe())
    df_rating.columns = df_rating.columns.droplevel()
    df_rating = df_rating[["mean", "min", "max"]] 
    plt.barh(
        y=df_rating.index.values,
        width=df_rating["max"].values - 1,
        left=df_rating["min"].values,
        height=0.9,
        color="lightgray",
        alpha=0.8,
    )   

    colors = [
        "tab:green" if value >= 3.0 else "tab:orange" for value in df_rating["mean"].values
    ]
    
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
    plt.savefig("docs/average_customer_rating.png")
    
    # Gráfico de distribución del peso
    plt.figure()
    df.Weight_in_gms.plot.hist(
        title="Shipping weight distribution",
        color="tab:orange",
        edgecolor="white",
    )
    plt.gca().spines["top"].set_visible(False)
    plt.gca().spines["right"].set_visible(False)
    plt.savefig("docs/weight_distribution.png")

    # Crear archivo index.html para el dashboard
    with open("docs/index.html", "w") as f:
        f.write("""
        <!DOCTYPE html>
        <html lang="es">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Dashboard de Envíos</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    text-align: center;
                }
                h1 {
                    color: #333;
                }
                .container {
                    display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                    gap: 20px;
                    margin-top: 20px;
                }
                .image-container {
                    width: 45%;
                    margin-bottom: 30px;
                }
                img {
                    width: 100%;
                    max-width: 600px;
                    height: auto;
                }
            </style>
        </head>
        <body>
            <h1>Dashboard de Envíos</h1>
            <div class="container">
                <div class="image-container">
                    <h2>Envíos por Almacén</h2>
                    <img src="shipping_per_warehouse.png" alt="Shipping per Warehouse">
                </div>
                <div class="image-container">
                    <h2>Modo de Envío</h2>
                    <img src="mode_of_shipment.png" alt="Mode of Shipment">
                </div>
                <div class="image-container">
                    <h2>Calificación Promedio del Cliente</h2>
                    <img src="average_customer_rating.png" alt="Average Customer Rating">
                </div>
                <div class="image-container">
                    <h2>Distribución del Peso</h2>
                    <img src="weight_distribution.png" alt="Weight Distribution">
                </div>
            </div>
        </body>
        </html>
        """)

    print("Dashboard generado en la carpeta 'docs'")

if __name__ == "__main__":
    pregunta_01()
