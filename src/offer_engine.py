HIGH_RISK = 0.6
MED_RISK = 0.35


def risk_level(risk):
    if risk >= HIGH_RISK:
        return 'high'
    elif risk >= MED_RISK:
        return 'medium'
    else:
        return 'low'


def make_offer(risk, sentiment=None, favorite_category=None, avg_order_value=None):
    level = risk_level(risk)
    cat = favorite_category if favorite_category else 'товаров'

    # скидка от уровня риска
    if level == 'high':
        discount = 15
    elif level == 'medium':
        discount = 8
    else:
        discount = 0

    # если в отзыве негатив - добавляю, такого клиента терять дороже всего
    if sentiment == 'negative':
        discount += 10
    # дорогих клиентов держу чуть сильнее
    if avg_order_value and avg_order_value > 300 and level != 'low':
        discount += 5
    if discount > 30:
        discount = 30   # больше не даём, уйдём в минус по марже

    # сами правила
    if level == 'high' and sentiment == 'negative':
        offer = 'retention_apology'
        msg = f'Извините за неприятный опыт. Дарим {discount}% на «{cat}» и приоритетную поддержку.'
    elif level == 'high':
        offer = 'retention_soft'
        msg = f'Скучаем по вам! Возвращайтесь - {discount}% на «{cat}».'
    elif level == 'medium':
        offer = 'targeted_reco'
        msg = f'Думаем вам понравится новое в «{cat}», плюс {discount}% на заказ.'
    else:
        if sentiment == 'positive':
            offer = 'loyalty_upsell'
            msg = f'Спасибо что вы с нами! Новинки в «{cat}» и программа лояльности.'
        else:
            offer = 'loyalty'
            msg = f'Рекомендуем новинки в «{cat}».'

    return {'offer_type': offer, 'risk_level': level, 'discount_pct': discount, 'message': msg}


# проверяю на нескольких клиентах из разных ситуаций
if __name__ == '__main__':
    clients = [
        {'risk': 0.85, 'sentiment': 'negative', 'favorite_category': 'cama_mesa_banho', 'avg_order_value': 120},
        {'risk': 0.78, 'sentiment': 'positive', 'favorite_category': 'informatica_acessorios', 'avg_order_value': 350},
        {'risk': 0.45, 'sentiment': None, 'favorite_category': 'beleza_saude', 'avg_order_value': 90},
        {'risk': 0.15, 'sentiment': 'positive', 'favorite_category': 'esporte_lazer', 'avg_order_value': 200},
    ]

    for c in clients:
        o = make_offer(**c)
        print(o['offer_type'], '| риск', o['risk_level'], '| скидка', o['discount_pct'], '%')
        print(o['message'])
        print()
