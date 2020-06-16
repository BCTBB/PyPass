# Preface
The scripts provided in this repository should be analyzed and used at the cloners discretion. While many of the scripts work as is, running a script without understanding of what it does can cause damage.

Prior to running any of the scripts, ensure that you understand and test the copy that you've cloned.

# Requirements
* Ubuntu 18.04.1 LTS (Mileage with other flavors may vary)
* MySQL

# Required software packages
```
apt-get install mysql-server
apt-get install python2.7
apt-get install python-mysqldb
```

# Python Pip Packages
```
pip install flask
pip install flask_wtf
pip install flask-mysql
```

# Create Database
```
create database EmpData;

use EmpData;

CREATE TABLE User(
userId INT NOT NULL AUTO_INCREMENT,
userName VARCHAR(100) NOT NULL,
password VARCHAR(40) NOT NULL,
code VARCHAR(32) NOT NULL,
date DATETIME NOT NULL DEFAULT '2011-01-26 14:30:00',
days int,
PRIMARY KEY(userId)
);
```

# Create Database User
```
GRANT ALL PRIVILEGES ON *.* TO 'mySecretUser'@'localhost' IDENTIFIED BY '<Password>';
```

# Running PyPass
```
python passwords.py
```
