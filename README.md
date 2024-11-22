# ***X-PYTHON***
![](/images/X-PYTHON.jpg)

# DECOMPRESS
![](/images/decompress.png)

## **Функціонал** :page_with_curl: **:**
+ ***Ця программа для аналізу великого набору даних (більше 1 мільйона рядків) у форматі CSV. Програма може: знаходити середнє, мінімальне, максимальне значення для заданих стовпців, а також робити фільтрацію даних. Обробка великих(більше 1 мільйона записів) CSV-файлів ресурсу.Обчислення базової статисти (середнє, мінімум, максимум) для обраних стовпців. Графічний інтерфейс для редагування даних в ресурсах Історія пошуку; Користувацькі фільтри; Діаграми для візуалізації даних;
Реалізувати можливість фільтрації за значеннями стовпців Повнотекстовий пошук; Фільтри з користувацькою умовою та стандартними(Більше, менше, дорівнює і т.д.); Забезпечення високої ефективністі для роботи з великими файлами (наприклад, через використання бібліотеки pandas).***

## **Як запустити?** :page_with_curl: **:**
+ ***Нічого особливого просто нажимаєте на кнопку пуску у файлі work_csv.py яка знаходиться на картинці і обведена ↓***
![](/images/run.png)

## Гайд як користуватися проєктом:
+ **1** ***У виведенному віконці першим що ви повинні зробити це загрузити якийсь csv, для цього треба нажати на кнопку: завантажити CSV, у мене є csv є у цьому проєкті, просто переходите до файлу в який ви зберігли цей проєкт переходите у папку csv_files і вибираєте якийсь місяць***
+ **2** ***Далі вам потрібно ввести у поле де підписанно назва ствобця, щось одне з Unnamed: 0,Unnamed: 1,Unnamed: 2,Unnamed: 3,Unnamed: 4,Unnamed: 5,Unnamed: 6,Unnamed: 7,Unnamed: 8,Unnamed: 9,Unnamed: 10,Unnamed: 11,Unnamed: 12,Unnamed: 13,Unnamed: 14,Unnamed: 15,Unnamed: 16,Unnamed: 17,Unnamed: 18,Unnamed: 19,Unnamed: 20,Unnamed: 21,Unnamed: 22,Unnamed: 23,Unnamed: 24,Unnamed: 25,Unnamed: 26,Unnamed: 27,Unnamed: 28,Unnamed: 29,Unnamed: 30,Unnamed: 31,Unnamed: 32, це все колонки які будуть перевірятися***
+ **3** ***Потім ви можете нажати на кнопку: статистика, щоб подивитись на результат, або можете ще більше зконкретизувати свій запит, написав ши у полі умова такі варанти: Більше, Менше або Дорівнює, і в іншому полі вводу под назвою значення записати число щоб код шукав числа з колонки більші менші або які будуть дорівнювати введеному вами числу, і щоб перевірити чи все ви правильно записали нажимаєте на кнопку сатистика, і якщо хочете переглянути гіпсограму, нажимаєте на однойменну кнопку***

# FastApi site
![](/images/FastApi_site.png)

## **Функціонал** :page_with_curl: **:**
+ ***ця программа створенна для аналізу фінансової звітності за 12 місяців. Програмна може: працювати з фронтендом(за допомогою кругових діаграм візуалізувати дані по місяцям, та за рік). Бекенд може бути Flask або FastApi***

## **Як запустити?** :page_with_curl: **:**
+ **1.** ***Відкриваємо термінал Ctrl + `***
+ **2.** ***Переходимо до папки app у якій все знаходиться***
```powershell
cd app/
```
+ **3.** ***Далі підключаємо venv є 2 способи як його підключити:***
+ 1
```powershell
.\.venv\Scripts\activate.ps1
```
+ 2
```powershell
.venv/Scripts/activate.ps1
```

+ **4.** ***Після того як venv підключенно, ми пишемо таку команду:***
```powershell
poetry run main
```
+ ***Чекаємо деякий час поки не зявиться ось такий шлях http://127.0.0.1:5050, але переходимо не за цим шлахом а зразу за ось цим: http://127.0.0.1:5050/docs, цей шлях для того щоб зразу опинитись у самому проєкті щоб перевірити роботу***

## Гайд як користуватися проєктом:
+ **1** ***Відкриваєте ендпоінт під назвою /upload, нажимаєте на try it out, потім у оплі де завантажити файл нажимаєте на кнопку і переходите по файлам до цього проєкту і знаходете файл Бюджет 1896.xlsx і нажимаєте завантажити, після того як ви завантажили вам покажуть усі місяці які було створенно***
+ **2** ***Далі переходите до наступного ендроінту під назвою /monthly_summary/ тут також нажимаєте на кнопку try it out і в полі записуєту місяць про який ви хочете дізнатися інформацію далі натискаєте на кнопку execute і отримуєту повниу інформацію за данними цього місяця***
+ **3** ***Далі переходите до наступного ендпоінту під назвою /yearly_summary/, тут знову ж натискаєте на try it out і потім просто execute і вам показує скільки було витраченно і отриманно, на цьому все, дякую за те що прочити до кінця, і на цьому все, дякую за увагу :)***