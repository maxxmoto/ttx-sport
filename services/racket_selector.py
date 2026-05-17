import csv
import os

rackets_data = []

def load_rackets():
    global rackets_data
    
    # Пробуем все возможные пути
    paths = [
        'data/rackets.csv',
        '/app/data/rackets.csv',
        os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'data', 'rackets.csv')
    ]
    
    file_path = None
    for path in paths:
        print(f"Проверяю: {path}")
        if os.path.exists(path):
            file_path = path
            print(f"Найден: {path}")
            break
    
    if not file_path:
        # Если не нашли - создаём файл из захардкоженных данных
        print("Файл не найден, создаю заново...")
        os.makedirs('data', exist_ok=True)
        file_path = 'data/rackets.csv'
        with open(file_path, 'w', encoding='utf-8', newline='') as f:
            f.write("type,brand,model,speed_class,speed,spin,control,weight,thickness,price_range,tensor,pimples\n")
            f.write("base,Butterfly,Timo Boll ALC,OFF,8.5,9.0,7.5,88,,3,,\n")
            f.write("base,Butterfly,Viscaria,OFF,8.7,8.8,7.8,90,,3,,\n")
            f.write("base,Stiga,Allround Classic,ALL,6.0,7.0,9.5,82,,1,,\n")
            f.write("base,DHS,Power G7,OFF,8.0,8.5,7.5,90,,2,,\n")
            f.write("rubber,Butterfly,Tenergy 05,,,,,2.1,3,1,0\n")
            f.write("rubber,Butterfly,Rozena,,,,,2.1,2,1,0\n")
            f.write("rubber,Palio,AK47 Red,,,,,2.0,1,1,0\n")
    
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            rackets_data.append(row)
    print(f"Загружено {len(rackets_data)} записей.")

def get_recommendation(answers: dict) -> str:
    bases = [r for r in rackets_data if r['type'] == 'base']
    rubbers = [r for r in rackets_data if r['type'] == 'rubber']

    level = answers.get('level', '')
    style = answers.get('style', '')
    speed_pref = answers.get('speed', '')
    spin_pref = answers.get('spin', '')
    budget = answers.get('budget', '')

    if 'beginner' in level:
        bases = [b for b in bases if b['speed_class'] in ('ALL', 'ALL+')]
    elif 'semi_pro' in level or 'professional' in level:
        bases = [b for b in bases if b['speed_class'] in ('OFF', 'OFF+')]
    else:
        bases = [b for b in bases if b['speed_class'] in ('ALL+', 'OFF-', 'OFF')]

    if 'defensive' in style:
        bases = [b for b in bases if b['speed_class'] == 'DEF']
    elif 'pimples' in style:
        bases = [b for b in bases if b['speed_class'] in ('ALL', 'DEF')]

    if 'control' in speed_pref:
        bases.sort(key=lambda x: float(x['control']), reverse=True)
    elif 'max' in speed_pref:
        bases.sort(key=lambda x: float(x['speed']), reverse=True)

    if 'high' in spin_pref:
        rubbers = [r for r in rubbers if float(r['spin']) >= 8.5]
    elif 'low' in spin_pref:
        rubbers = [r for r in rubbers if float(r['spin']) <= 7.5]

    budget_map = {'budget_low': 1, 'budget_medium': 2, 'budget_high': 3, 'budget_unlimited': 99}
    max_price = budget_map.get(budget, 99)
    if max_price < 99:
        bases = [b for b in bases if int(b['price_range']) <= max_price]
        rubbers = [r for r in rubbers if int(r['price_range']) <= max_price]

    weight_pref = answers.get('weight', 'weight_any')
    if 'light' in weight_pref:
        bases = [b for b in bases if int(b.get('weight', 0)) <= 80]
    elif 'medium' in weight_pref:
        bases = [b for b in bases if 80 <= int(b.get('weight', 0)) <= 90]
    elif 'heavy' in weight_pref:
        bases = [b for b in bases if int(b.get('weight', 0)) >= 90]

    if not bases:
        return "К сожалению, не удалось подобрать основание под ваши параметры."
    if not rubbers:
        rubbers = [r for r in rackets_data if r['type'] == 'rubber']

    base = bases[0]
    fh_rub = rubbers[0]
    bh_rub = rubbers[1] if len(rubbers) > 1 else fh_rub

    text = "🎯 <b>Рекомендуемая сборка:</b>\n\n"
    text += f"Основание: {base['brand']} {base['model']} (класс {base['speed_class']}, вес {base['weight']}г)\n"
    text += f"Накладка FH: {fh_rub['brand']} {fh_rub['model']} {fh_rub['thickness']}мм (вращение {fh_rub['spin']})\n"
    text += f"Накладка BH: {bh_rub['brand']} {bh_rub['model']} {bh_rub['thickness']}мм (контроль {bh_rub['control']})\n"
    text += f"\nОриентировочная цена: {'бюджетная' if max_price==1 else 'средняя' if max_price==2 else 'высокая'}"
    return text
