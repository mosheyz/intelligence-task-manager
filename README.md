# intelligence-task-manager

מערכת לניהול משימות מודיעין של סוכנים. <br>
המערכת מנהלת את פרטי הסוכנים, ואת פרטי ורמת המשימות. <br>
הרצה באמצעות שרת FastAPI, ועבודה עם מסדי נתונים באמצעות MySQL. <br>

## מבנה התיקיות

```
intelligence-task-manager/
├── database/
│   ├── db_connection.py
│   ├── base_db.py
│   ├── agent_db.py
│   └── mission_db.py
├── README.md
├── requirements.txt
└── .gitignore

```

## מבנה הטבלאות
### טבלת agents:

|field|type|constraint
|-----|----|----------|
|id|INT|AUTO_INCREMENT PRIMARY KEY|
|name|VARCHAR|NOT NULL|
|specialty|VARCHAR|NOT NULL|
|is_active|BOOLEAN|DEFAULT TRUE NOT NULL|
|completed_missions|INT|DEFAULT 0|
|failed_missions|INT|DEFAULT 0|
|agent_rank|ENUM| (Junior, Senior, Commander)

### טבלת missions:

|field|type|constraint
|-----|----|----------|
|id|INT|AUTO_INCREMENT PRIMARY KEY|
|title|VARCHAR|NUT NULL|
|description|TEXT|NUT NULL|
|location|VARCHAR|NOT NULL|
|difficulty|INT|1 - 10|
|importance|INT|1 - 10|
|status|ENUM| (new, assigned, in_progress, completed, failed, cancelled)
|risk_level|VARCHAR|NOT NULL|
|assigned_agent_id|int|


## הסבר על מבנה המחלקות

### מחלקת DB:

אחראי על החיבור הראשוני לdatabase, ועל יצירת הטבלאות. <br>
מתודות:

* get_connection => חיבור ראשוני ל container
* create_database => יצירת database אם לא קיים.
* create_tables => יוצר טבלאות אם לא קיימות.

יוצר אובייקט ראשוני שמפעיל את החיבור בהרצה של התוכנית

### מחלקת BaseDB:

אחראי על שליחת שאילתות ב SQL על פי בקשת המשתמש.
מקבל בinit שם טבלה.
כולל מתודות בסיסיות של CRUD, ללא שאילתות שמיוחדות לטבלה מסויימת.
משתמש באובייקט החיבור שנוצר ב DB/ <br>

מתודות:
* create => מקבלת data, יוצר שורה חדשה בטבלה - בהתאם לשם הטבלה שקיבל.
* get_all => מחזיר רשימה של כל השורות בטבלה.
* get_by_id => מקבלת id, מחזיר שורה ע"פ ה id שלה.
* update => מקבלת id, data, עורך שורה בטבלה.

### מחלקת AgentDB:

אחראי על מימוש בקשות מהמשתמש לבצע על טבלת agents.
יורש את המתודות הבסיסיות ממחלקת Base DB, ומודיף את המתודות המיוחדות לו. <br>

מתודות:
* deactivate_agent => מקבלת id, ומשתמש במתודה update על מנת לשנות את שדה is_active = False
* increment_completed => מקבלת id, מעלה את שדה complete_missions ב1.
* increment_failed => מקבלת id, מעלה את שדה failed_missions ב1.
* get_agent_performance => מקבלת id, מחזירה מילון עם המפתחות האלו completed, failed, total, success_rate עבור הסוכן.
* count_active_agents => מחזירה את מספר הסוכנים הפעילים.

### מחלקת MissionDB:
 
אחראי על מימוש בקשות מהמשתמש לבצע על טבלת missions.
יורש את המתודות הבסיסיות ממחלקת Base DB, ומודיף את המתודות המיוחדות לו. <br>

מתודות:
* assign_mission => מקבלת m_id, a_id, ומשתמש במתודה update על מנת לשנות assigned_agent_id בהתאם.
* update_mission_status => מקבלת id, status, ומשתמש במתודה update על מנת לשנות בהתאם.
* get_open_missions_by_agent => מקבלת id, ומחזירה רשימת משימות פעילות.
* count_all_missions => מחזירה סה"כ משימות.
* count_by_status => מחזירה סה"כ לפי סטטוס מסויים.
* count_open_missions => מחזירה סה"כ משימות פתוחות.
* count_critical_missions => מחזירה סה"כ משימות ברמת CRITICAL.
* get_top_agent =>  מחזירה את הסוכן עם completed_missions הגבוה ביותר.


## חוקי המערכת

|מספר|פרטי החוק
|---|---|
|1|rank חייב להיות Junior / Senior / Commander - כל ערך אחר זורק שגיאה.
|2|difficulty ו-importance חייבים להיות בין 1 ל-10.
|3|risk_level מחושב אוטומטית בעת יצירת משימה - המשתמש לא שולח אותו.
|4|סוכן עם is_active=False לא יכול לקבל משימות.
|5|סוכן לא יכול להחזיק יותר מ-3 משימות פתוחות (ASSIGNED / IN_PROGRESS) במקביל.
|6|אם risk_level=CRITICAL - רק סוכן בדרגת Commander יכול לקבל את המשימה.
|7|ניתן לשייך רק משימה בסטטוס NEW. לאחר שיוך: status=ASSIGNED.
|8|ניתן להתחיל רק משימה בסטטוס ASSIGNED. לאחר התחלה: status=IN_PROGRESS.
|9|ניתן לסיים רק משימה: IN_PROGRESS  ולשנות לסטטוס failed or completed
|10|ניתן לבטל רק משימה בסטטוס NEW או ASSIGNED.


## הוראות הרצה

```text

pip install mysql-connector-python

docker run -d --name intelligence-mysql -e MYSQL_ROOT_PASSWORD=1234 -e MYSQL_DATABASE=Intelligence_db -p 3306:3306 mysql:8.0

docker exec -it intelligence-mysql mysql -uroot -p1234

