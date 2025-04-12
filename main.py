import sys
import importlib
from models.black_scholes import black_scholes
from models.implied_volatility import implied_volatility
from models.geometric_asian import geometric_asian
from models.arithmetic_asian_mc import arithmetic_asian_mc
from models.geometric_basket import geometric_basket
from models.arithmetic_basket_mc import arithmetic_basket_mc
from models.american_binomial import american_binomial
from models.kiko_quasi_mc import kiko_quasi_mc

def main():
    while True:
        print("\nMini Option Pricer")
        print("===================")
        print("Select a model to run:")
        print("1. European Option (Black-Scholes)")
        print("2. Implied Volatility")
        print("3. Geometric Asian Option")
        print("4. Arithmetic Asian Option (Monte Carlo)")
        print("5. Geometric Basket Option")
        print("6. Arithmetic Basket Option (Monte Carlo)")
        print("7. American Option (Binomial Tree)")
        print("8. KIKO Put Option (Quasi-Monte Carlo)")
        print("0. Exit")

        choice = input("\nEnter your choice: ").strip()

        try:
            if choice == "1":
                importlib.reload(black_scholes)  # Reload the module
                black_scholes.run()
            elif choice == "2":
                importlib.reload(implied_volatility)
                implied_volatility.run()
            elif choice == "3":
                importlib.reload(geometric_asian)
                geometric_asian.run()
            elif choice == "4":
                importlib.reload(arithmetic_asian_mc)
                arithmetic_asian_mc.run()
            elif choice == "5":
                importlib.reload(geometric_basket)
                geometric_basket.run()
            elif choice == "6":
                importlib.reload(arithmetic_basket_mc)
                arithmetic_basket_mc.run()
            elif choice == "7":
                importlib.reload(american_binomial)
                american_binomial.run()
            elif choice == "8":
                importlib.reload(kiko_quasi_mc)
                kiko_quasi_mc.run()
            elif choice == "0":
                print("Exiting.")
                sys.exit(0)
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"Error running the selected model: {str(e)}")
            print("Please try again.")

if __name__ == "__main__":
    main()
