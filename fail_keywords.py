import pandas as pd
import os
import base64
import io

new_dataframe = pd.DataFrame()

ekb = {
    'path' : 'datas/Екатеринбург2',
    'tags_for_del' : ['дом маева'],
    'path_del' : 'datas/Екатеринбург_Плохие',
    'path_add' : ['datas/Екатеринбург/Дом Маева']
}

vlad = {
    'path' : 'datas/Владимир2',
    'tags_for_del' : [
        'Владимир', 'П.И. Чайковский', 'Танкистам', '1941-1945', 'Кресень', 'Бобёр', 'Венера',
        'Наука', 'Дева Мария', 'Площадка на крыше', 'Пожарный автомобиль-лестница', 'Лебедев-Полянский П.И.',
        'Старинный велосипед', 'Такса', 'Воинам-интернационалистам', 'Макет ракеты-носителя Союз-ТМ', 'Чернобыль - трагедия XX века',
        '2000 летию Рождества Христова', 'Сердце', 'église arménienne de Vladimir',
        'Владимирская гвардейская ракетная Витебская Краснознамённая армия', 'Панно на фасаде', 'Погибшим в ВОВ', 'Каменная горка',
        'Мальчик с рогаткой', 'Великая Княгиня Ольга', 'Библиотечная лужайка', 'Кино 9D', 'Филёр', 'Фавор', 'Художник на пленэре',
        'Владимирским железнодорожникам погибшим в ВОВ'
    ],
    'path_del' : 'datas/Владимир_Плохие',
    'path_add' : [
        'datas/Владимир/1941-1945', 'datas/Владимир/2000 летию Рождества Христова', 'datas/Владимир/église arménienne de Vladimir',
        'datas/Владимир/Бобёр', 'datas/Владимир/Венера', 'datas/Владимир/Владимир', 'datas/Владимир/Воинам-интернационалистам',
        'datas/Владимир/Дева Мария', 'datas/Владимир/Кресень', 'datas/Владимир/Лебедев-Полянский П.И',
        'datas/Владимир/Макет ракеты-носителя Союз-ТМ', 'datas/Владимир/Мальчик с рогаткой', 'datas/Владимир/Наука',
        'datas/Владимир/П.И. Чайковский', 'datas/Владимир/Панно на фасаде', 'datas/Владимир/Площадка на крыше',
        'datas/Владимир/Погибшим в ВОВ', 'datas/Владимир/Пожарный автомобиль-лестница',
        'datas/Владимир/Старинный велосипед', 'datas/Владимир/Такса', 'datas/Владимир/Танкистам', 'datas/Владимир/Филёр',
        'datas/Владимир/Художник на пленэре', 'datas/Владимир/Чернобыль - трагедия XX века'
    ]
}

nn = {
    'path' : 'datas/Нижний Новгород2',
    'tags_for_del' : ['Усадьба Киршбаумов', 'Дом В. С. Прядилова'],
    'path_del' : 'datas/НижнийНовгород_Плохие',
    'path_add' : [],
    'swap' : {
        'Церковь в честь Рождества Богородицы' : 'Рождественская церковь',
        'Дмитриевская башня' : 'Дмитровская башня'
    }
}

yarik = {
    'path' : 'datas/Ярославль2',
    'tags_for_del' : [],
    'path_del' : 'datas/Ярослав_Плохие',
    'path_add' : []
}

cities = [nn, ekb, vlad, yarik]

import os
from PIL import Image
import pandas as pd

df = pd.DataFrame(columns=['city', 'name', 'image'])

for city in cities:
    count = 0
    image_files = os.listdir(city['path'])
    for image_file in image_files:
        flag = True
        for tag in city['tags_for_del']:
            if tag == ''.join(image_file.split('.')[0].split('_')[-1]).lower():
                flag = False

        if image_file in os.listdir(city['path_del']):
            continue
        
        if not image_file.split('.')[-1] in ['jpg', 'webm', 'jpeg', 'png'] or not '.' in image_file:
            continue

        if flag:
            with open(os.path.join(city['path'], image_file), "rb") as file:
                image_data = file.read()
            
            base64_image = base64.b64encode(image_data).decode("utf-8")
            
            if 'swap' in city and ''.join(image_file.split('.')[0].split('_')[-1]) in city['swap']:
                df = df.append({'city' : os.path.basename(city['path'][0:-1]), 'name': city['swap'][''.join(image_file.split('.')[0].split('_')[-1])], 'image': base64_image}, ignore_index=True)
            else:
                df = df.append({'city' : os.path.basename(city['path'][0:-1]), 'name': ''.join(image_file.split('.')[0].split('_')[-1]), 'image': base64_image}, ignore_index=True)

    for tag in city['path_add']:
        add_images_file = os.listdir(tag)
        
        for image_file in add_images_file:
            if not image_file.split('.')[-1] in ['jpg', 'webm', 'jpeg', 'png'] or not '.' in image_file:
                continue

            with open(os.path.join(tag, image_file), "rb") as file:
                image_data = file.read()

            base64_image = base64.b64encode(image_data).decode("utf-8")
            df = df.append({'city' : os.path.basename(city['path'][0:-1]), 'name': os.path.basename(tag).capitalize(), 'image': base64_image}, ignore_index=True)

    df.to_csv(city['path'] + '.csv', index=False)

df = df.drop_duplicates(subset='image', ignore_index=True)

import numpy as np
print('\n')
for i in set(df['city']):
    new_df = df[(df['city'] == i)]
    print(i + ':')
    print('- Количество мест:', len(set(new_df['name'])))
    print('- Количество изображений:', len(new_df['image']), '\n')

print('Всего:')
print('- Количество мест:', len(set(df['name'])))
print('- Количество изображений:', len(df['image']))

print('\n\n', df)

df.to_csv('all.csv')