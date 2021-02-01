# Routine
A Program For Routine Manage, A Small Web Site


# DataBase Design

## 1. Book Table
| Field | Type | Comment |
| --- | --- | --- |
| Slug | CharField | |
| Name | CharField | |
| Author | CharField | |
| Cover | ImageField | |
| Data | FileField | |

## 2. User Table
| Field | Type | Comment |
| --- | --- | --- |
| Slug | CharField | |
| Account | CharField | |
| Password | CharField | |
| Name | CharField | |
| Birthday | DateField | |
| Email | EmailField | |
| Phone | CharField | |

## 3. Log Table

| Field | Type | Comment |
| --- | --- | --- |
| Slug | CharField | |
| User | CharField | |
| Operate | EnumField | |
| Date | DateField | |
| Result | EnumField | |


# Api Design

## 1. Upload The Book Resource
### Method: POST /book
| RequestField | Type | Comment |
| --- | --- | --- |
| Name | CharField | |
| Author | CharField | |
| Data | EnumField | |


## 2. Get The Book Resource
### Method: GET /book
| RequestField | Type | Comment |
| --- | --- | --- |
| Slug | CharField | |


## 3. Login In
### Method: GET /user
| RequestField | Type | Comment |
| --- | --- | --- |
| Account | CharField | |
| Password | CharField | |

## 4. Register
### Method: GET /user
| RequestField | Type | Comment |
| --- | --- | --- |
| Account | CharField | |
| Password | CharField | |