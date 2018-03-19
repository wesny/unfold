import rules

@rules.predicate
def is_buyer(user, purchase):
    return purchase.buyer == user

@rules.predicate
def is_publisher(user, purchase):
    return purchase.publisher == user

rules.add_perm('transactions.retrieve_purchase', is_buyer | is_publisher | rules.is_superuser)

