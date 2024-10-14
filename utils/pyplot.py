import matplotlib.pyplot as plt


def show_graph(name: list[str], transactions: list[int], xlabel: str) -> None:
    plt.bar(name, transactions, color='blue')

    plt.xlabel(xlabel)
    plt.ylabel('Transaction Amount')
    plt.title('Transactions')

    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show(block=False)
