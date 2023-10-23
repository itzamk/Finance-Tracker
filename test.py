from investment_database import get_asset_details

asset_details, transaction_history = get_asset_details('bitcoin')

def calculate_metrics(transaction_history):
        total_cost = 0
        total_amount = 0

        for transaction in transaction_history:
            if transaction[4] == 'buy':
                total_cost += transaction[2] * transaction[3]  # price * amount
                total_amount += transaction[3]  # amount
            elif transaction[4] == 'sell':
                total_cost -= transaction[2] * transaction[3]  # price * amount
                total_amount -= transaction[3]  # amount

        unrealized_gains = total_amount * asset_details[3] - total_cost  # Assume current_price is known
        roi = (unrealized_gains / total_cost) * 100 if total_cost != 0 else 0  # Protect against division by zero

        return total_cost, unrealized_gains, roi

print(calculate_metrics(transaction_history)[0])