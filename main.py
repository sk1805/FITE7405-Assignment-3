import sys
import importlib

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
                import black_scholes
                importlib.reload(black_scholes)  # Reload the module
                black_scholes.run()
            elif choice == "2":
                import implied_volatility
                importlib.reload(implied_volatility)
                implied_volatility.run()
            elif choice == "3":
                import geometric_asian
                importlib.reload(geometric_asian)
                geometric_asian.run()
            elif choice == "4":
                import arithmetic_asian_mc
                importlib.reload(arithmetic_asian_mc)
                arithmetic_asian_mc.run()
            elif choice == "5":
                import geometric_basket
                importlib.reload(geometric_basket)
                geometric_basket.run()
            elif choice == "6":
                import arithmetic_basket_mc
                importlib.reload(arithmetic_basket_mc)
                arithmetic_basket_mc.run()
            elif choice == "7":
                import american_binomial
                importlib.reload(american_binomial)
                american_binomial.run()
            elif choice == "8":
                import kiko_quasi_mc
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
