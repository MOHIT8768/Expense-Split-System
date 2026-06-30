def split_equal(amount, members):
    share = amount / len(members)    
    result = {}
    for m in members:
        result[m] = round(share, 2)
    return result
def calculate_balances(expenses, members):
    total_paid = {}
    for m in members:
        total_paid[m] = 0
    for exp in expenses:
        payer = exp["paid_by"]
        amount = exp["amount"]
        total_paid[payer] += amount
    total_amount = sum(total_paid.values())
    share = total_amount / len(members)
    balances = {}
    for m in members:
        balances[m] = total_paid[m] - share
    return balances
def simplify_debts(balances):
    creditors = []
    debtors = []
    for person, amount in balances.items():
        if amount > 0:
            creditors.append([person, amount])
        elif amount < 0:
            debtors.append([person, -amount])
    result = []
    i, j = 0, 0
    while i < len(debtors) and j < len(creditors):
        debtor, debt = debtors[i]
        creditor, credit = creditors[j]
        settle_amount = min(debt, credit)
        result.append({
            "from": debtor,
            "to": creditor,
            "amount": round(settle_amount, 2)
        })
        debtors[i][1] -= settle_amount
        creditors[j][1] -= settle_amount
        if debtors[i][1] == 0:
            i += 1
        if creditors[j][1] == 0:
            j += 1
    return result