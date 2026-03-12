# -*- coding: utf-8 -*-
#
# 🟢 โค้ดฉบับอัปเดต: Hybrid Menu - รูปใหญ่, ถามจำนวน, เรียงตะกร้าใหม่
# 🟢 อัปเดตล่าสุด: เพิ่มหน้าเงิน, แก้ Flow หน้ารวม, ลบราคาออกจากหน้าเพิ่ม
#
# 🟢 อัปเดต (Gemini): (1) แก้ไขหน้า Admin Edit เป็นหน้าจัดการโต๊ะ
# 🟢 อัปเดต (Gemini): (2) เปลี่ยน UI หน้า Admin ให้เหมือนหน้าโต๊ะ + เพิ่มปุ่ม "แก้ไข"
# 🟢 อัปเดต (Gemini): (3) [Admin] เพิ่มปุ่มกลับหน้ารวม, [Login] Staff ไปหน้า Admin ทันที
# 🟢 อัปเดต (Gemini): (4) แก้เวลา Order, แก้ปุ่มลัด Login, แก้การเพิ่ม/แสดงผลเมนู
#
# 🟢 อัปเดต (User): (1) [Login] Staff เปลี่ยนไปหน้า 'หน้ารวม' (summary_page)
# 🟢 อัปเดต (User): (2) [Login] ปุ่มลัด (679,642) เปลี่ยนไปหน้า 'หน้าแก้' (fix_page)
# 🟢 อัปเดต (User): (3) เพิ่ม 'หน้าแก้.png' เป็นหน้าใหม่
#
# 🟢 อัปเดต (Gemini): (5) [Fix Page] 'หน้าแก้' เพิ่มช่องกรอก Username/Password เพื่อไปหน้า Profile
#
# 🟢 อัปเดต (Gemini): (6) [Money Page] เปลี่ยนเป็นช่องกรอกจำนวนคน, ไปหน้าบิล
# 🟢 อัปเดต (Gemini): (7) [Payment Popup] เปลี่ยน QR Code เป็น .jpg
#
# 🟢 อัปเดต (Gemini): (8) [Money Page] เปลี่ยนเป็นปุ่มคลิก 1-6+ คน (ตาม User Request)
# 🟢 อัปเดต (Gemini): (9) [Bill Page] เพิ่มหน้าบิล (Mooay Noi) และเชื่อมปุ่มยืนยัน QR (ตาม User Request)

import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog
import shutil
from PIL import Image, ImageTk
import os
from collections import defaultdict
import sqlite3
import datetime # 🟢 NEW: สำหรับจัดการเวลา
# 🟢 NEW: (เพิ่ม) สำหรับแก้ไขเวลา
from datetime import timedelta 

# --------------------------------------------------------------------------------------
# หมวดที่ 1: การตั้งค่าเริ่มต้นและการนำเข้าไลบรารี
# --------------------------------------------------------------------------------------

# --- หมวดที่ 2: การตั้งค่าและค่าคงที่ (Configuration & Constants) ---
BASE_DIR = os.path.normpath(r"D:\Code_Python\โปรเจคจร้า") # <- Adjust this path if needed

# 🟢 Database Settings
DATABASE_NAME = "Database.db"
DATABASE_PATH = os.path.join(BASE_DIR, DATABASE_NAME)

# ⭐️ Profile Image Folder
PROFILE_DIR = os.path.join(BASE_DIR, "Profile")

IMAGE_PATHS = {
    "table_page_bg": os.path.join(BASE_DIR, "หน้าโต๊ะ.png"),
    "login_bg": os.path.join(BASE_DIR, "หน้าเข้าใช้.png"),
    "food_menu_bg": os.path.join(BASE_DIR, "หน้าหลัก.png"), 
    "order_list_bg": os.path.join(BASE_DIR, "หน้ารายการอาหาร.png"),
    "summary_page_bg": os.path.join(BASE_DIR, "หน้ารวม.png"), 
    "register_bg": os.path.join(BASE_DIR, "หน้าสมัคร.png"),
    "forgot_bg": os.path.join(BASE_DIR, "หน้าลืม.png"),
    "admin_edit_bg": os.path.join(BASE_DIR, "หน้าเจ้าหน้าที่.png"),
    "profile_page_bg": os.path.join(BASE_DIR, "หน้าโปรไฟล์.png"),
    "add_item_page_bg": os.path.join(BASE_DIR, "หน้าเพิ่ม.png"),
    "placeholder_image": os.path.join(BASE_DIR, "กล้อง.png"),
    "order_status_page_bg": os.path.join(BASE_DIR, "หน้าorder.png"),
    "money_page_bg": os.path.join(BASE_DIR, "หน้าเงิน.png"),
    "bill_page_bg": os.path.join(BASE_DIR, "หน้าบิล.png"), # 🟢 NEW: (เพิ่ม) หน้าบิล
    "fix_page_bg": os.path.join(BASE_DIR, "หน้าแก้.png") # 🟢 NEW: (เพิ่ม) หน้าแก้
}

WINDOW_WIDTH = 1000
WINDOW_HEIGHT = 800
WINDOW_SIZE = f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"

CATEGORY_OPTIONS = ["เลือกประเภท...", "เนื้อ", "อาหารทะเล", "ผักผลไม้", "ของทานเล่น", "ของหวาน"]

# --- หมวดที่ 3: พิกัดพื้นที่ที่คลิกได้ (อ้างอิงจากภาพต้นฉบับ) ---
ORIG_MENU_PROFILE_BOX = {"x": 1242, "y": 18, "width": 100, "height": 100}

# --- หมวดที่ 4: หน้าล็อกอิน (Login Page) ---
ORIG_LOGIN_USERNAME_LABEL = {"x": 450, "y": 250, "width": 150, "height": 30}
ORIG_LOGIN_USERNAME_BOX = {"x": 450, "y": 285, "width": 460, "height": 60}
ORIG_LOGIN_PASSWORD_LABEL = {"x": 450, "y": 350, "width": 150, "height": 30}
ORIG_LOGIN_PASSWORD_BOX = {"x": 450, "y": 385, "width": 460, "height": 60}
NEW_LOGIN_CENTER_X = 675
NEW_LOGIN_CENTER_Y = 523
NEW_LOGIN_W_HALF = 150
NEW_LOGIN_H_HALF = 30
NEW_LOGIN_BUTTON_REGION = {
    "x_start": NEW_LOGIN_CENTER_X - NEW_LOGIN_W_HALF, "x_end": NEW_LOGIN_CENTER_X + NEW_LOGIN_W_HALF,
    "y_start": NEW_LOGIN_CENTER_Y - NEW_LOGIN_H_HALF, "y_end": NEW_LOGIN_CENTER_Y + NEW_LOGIN_H_HALF
}
LOGIN_BUTTON_REGION = {"x_start": 440, "x_end": 840, "y_start": 590, "y_end": 690}
REG_CENTER_X = 1076; REG_CENTER_Y = 642; REG_CLICK_W_HALF = 100; REG_CLICK_H_HALF = 50
REGISTER_BUTTON_REGION = {
    "x_start": REG_CENTER_X - REG_CLICK_W_HALF, "x_end": REG_CENTER_X + REG_CLICK_W_HALF,
    "y_start": REG_CENTER_Y - REG_CLICK_H_HALF, "y_end": REG_CENTER_Y + REG_CLICK_H_HALF
}
FOR_CENTER_X = 264; FOR_CENTER_Y = 642; FOR_CLICK_W_HALF = 100; FOR_CLICK_H_HALF = 50
FORGOT_BUTTON_REGION = {
    "x_start": FOR_CENTER_X - FOR_CLICK_W_HALF, "x_end": FOR_CENTER_X + FOR_CLICK_W_HALF,
    "y_start": FOR_CENTER_Y - FOR_CLICK_H_HALF, "y_end": FOR_CENTER_Y + FOR_CLICK_H_HALF
}
ADMIN_EDIT_CENTER_X = 262
ADMIN_EDIT_CENTER_Y = 194
ADMIN_EDIT_W_HALF = 90
ADMIN_EDIT_H_HALF = 40
ADMIN_EDIT_BUTTON_REGION = {
    "x_start": ADMIN_EDIT_CENTER_X - ADMIN_EDIT_W_HALF, "x_end": ADMIN_EDIT_CENTER_X + ADMIN_EDIT_W_HALF,
    "y_start": ADMIN_EDIT_CENTER_Y - ADMIN_EDIT_H_HALF, "y_end": ADMIN_EDIT_CENTER_Y + ADMIN_EDIT_H_HALF
}

# 🟢 (แก้ไข) ปุ่มลัดไปหน้า "แก้" จากหน้า Login (X: 678 , Y: 641)
LOGIN_GOTO_ADMIN_CENTER_X = 678
LOGIN_GOTO_ADMIN_CENTER_Y = 641
LOGIN_GOTO_ADMIN_W_HALF = 100 # (ตั้งค่า W/H ประมาณ)
LOGIN_GOTO_ADMIN_H_HALF = 40
LOGIN_GOTO_ADMIN_REGION = {
    "x_start": LOGIN_GOTO_ADMIN_CENTER_X - LOGIN_GOTO_ADMIN_W_HALF, "x_end": LOGIN_GOTO_ADMIN_CENTER_X + LOGIN_GOTO_ADMIN_W_HALF,
    "y_start": LOGIN_GOTO_ADMIN_CENTER_Y - LOGIN_GOTO_ADMIN_H_HALF, "y_end": LOGIN_GOTO_ADMIN_CENTER_Y + LOGIN_GOTO_ADMIN_H_HALF
}

# ----------------------------------------------------------------------
# 🟢 START: (แก้ไข 3) และ (แก้ไข 4) (หน้าแก้)
# ----------------------------------------------------------------------
# 🟢 (เพิ่ม 3) พิกัดปุ่มยืนยัน "หน้าแก้" (X: 1181 , Y: 624)
FIX_CONFIRM_CENTER_X = 1181
FIX_CONFIRM_CENTER_Y = 624
FIX_CONFIRM_W_HALF = 150 # (ใช้ขนาดเดียวกับปุ่ม Login)
FIX_CONFIRM_H_HALF = 30 # (ใช้ขนาดเดียวกับปุ่ม Login)
FIX_PAGE_CONFIRM_REGION = {
    "x_start": FIX_CONFIRM_CENTER_X - FIX_CONFIRM_W_HALF, "x_end": FIX_CONFIRM_CENTER_X + FIX_CONFIRM_W_HALF,
    "y_start": FIX_CONFIRM_CENTER_Y - FIX_CONFIRM_H_HALF, "y_end": FIX_CONFIRM_CENTER_Y + FIX_CONFIRM_H_HALF
}

# 🟢 (เพิ่ม 4) พิกัดช่องกรอก "หน้าแก้" (ขยับ Y ลง 100)
FIX_PAGE_Y_OFFSET = 100
ORIG_FIX_USERNAME_LABEL = {"x": 450, "y": 250 + FIX_PAGE_Y_OFFSET, "width": 150, "height": 30}
ORIG_FIX_USERNAME_BOX = {"x": 450, "y": 285 + FIX_PAGE_Y_OFFSET, "width": 460, "height": 60}
ORIG_FIX_PASSWORD_LABEL = {"x": 450, "y": 350 + FIX_PAGE_Y_OFFSET, "width": 150, "height": 30}
ORIG_FIX_PASSWORD_BOX = {"x": 450, "y": 385 + FIX_PAGE_Y_OFFSET, "width": 460, "height": 60}
# ----------------------------------------------------------------------
# 🟢 END: (แก้ไข 3) และ (แก้ไข 4)
# ----------------------------------------------------------------------

# --- หมวดที่ 5: หน้าลงทะเบียน (Register Page) ---
REG_L_COL_X = 318
REG_R_COL_X = 706
REG_BOX_W = 310
REG_BOX_H = 55
REG_LBL_H = 30
ORIG_REG_USERNAME_LABEL = {"x": REG_L_COL_X, "y": 269, "width": REG_BOX_W, "height": REG_LBL_H}
ORIG_REG_USERNAME_BOX   = {"x": REG_L_COL_X, "y": 300, "width": REG_BOX_W, "height": REG_BOX_H}
ORIG_REG_PHONE_LABEL    = {"x": REG_R_COL_X, "y": 269, "width": REG_BOX_W, "height": REG_LBL_H}
ORIG_REG_PHONE_BOX      = {"x": REG_R_COL_X, "y": 300, "width": REG_BOX_W, "height": REG_BOX_H}
ORIG_REG_PASSWORD1_LABEL= {"x": REG_L_COL_X, "y": 404, "width": REG_BOX_W, "height": REG_LBL_H}
ORIG_REG_PASSWORD1_BOX  = {"x": REG_L_COL_X, "y": 435, "width": REG_BOX_W, "height": REG_BOX_H}
ORIG_REG_EMAIL_LABEL    = {"x": REG_R_COL_X, "y": 404, "width": REG_BOX_W, "height": REG_LBL_H}
ORIG_REG_EMAIL_BOX      = {"x": REG_R_COL_X, "y": 435, "width": REG_BOX_W, "height": REG_BOX_H}
ORIG_REG_PASSWORD2_LABEL= {"x": REG_L_COL_X, "y": 539, "width": REG_BOX_W, "height": REG_LBL_H}
ORIG_REG_PASSWORD2_BOX  = {"x": REG_L_COL_X, "y": 570, "width": REG_BOX_W, "height": REG_BOX_H}
ORIG_REG_PROFILE_BOX = {"x": 710, "y": 530, "width": 150, "height": 150}
REG_CONFIRM_CENTER_X = 1172; REG_CONFIRM_CENTER_Y = 618; REG_CONFIRM_W_HALF = 50; REG_CONFIRM_H_HALF = 25
REGISTER_CONFIRM_BUTTON_REGION = {
    "x_start": REG_CONFIRM_CENTER_X - REG_CONFIRM_W_HALF, "x_end": REG_CONFIRM_CENTER_X + REG_CONFIRM_W_HALF,
    "y_start": REG_CONFIRM_CENTER_Y - REG_CONFIRM_H_HALF, "y_end": REG_CONFIRM_CENTER_Y + REG_CONFIRM_H_HALF
}

# --- หมวดที่ 6: หน้าลืมรหัสผ่าน (Forgot Page) ---
FORGOT_BOX_W = 400; FORGOT_BOX_H = 60; FORGOT_LBL_H = 30
ORIG_FORGOT_EMAIL_LABEL = {"x": 475, "y": 324, "width": FORGOT_BOX_W, "height": FORGOT_LBL_H}
ORIG_FORGOT_EMAIL_BOX   = {"x": 475, "y": 355, "width": FORGOT_BOX_W, "height": FORGOT_BOX_H}
ORIG_FORGOT_PHONE_LABEL = {"x": 475, "y": 487, "width": FORGOT_BOX_W, "height": FORGOT_LBL_H}
ORIG_FORGOT_PHONE_BOX   = {"x": 475, "y": 518, "width": FORGOT_BOX_W, "height": FORGOT_BOX_H}
FORGOT_CONFIRM_CENTER_X = 1174; FORGOT_CONFIRM_CENTER_Y = 622; FORGOT_CONFIRM_W_HALF = 50; FORGOT_CONFIRM_H_HALF = 25
FORGOT_CONFIRM_BUTTON_REGION = {
    "x_start": FORGOT_CONFIRM_CENTER_X - FORGOT_CONFIRM_W_HALF, "x_end": FORGOT_CONFIRM_CENTER_X + FORGOT_CONFIRM_W_HALF,
    "y_start": FORGOT_CONFIRM_CENTER_Y - FORGOT_CONFIRM_H_HALF, "y_end": FORGOT_CONFIRM_CENTER_Y + FORGOT_CONFIRM_H_HALF
}

# --- หมวดที่ 7: หน้าแก้ไขของแอดมิน (Admin Edit Page) ---
# 🟢 NEW: ปุ่ม "แก้ไข" (ปุ่มกลาง) ในหน้า Admin (X: 681 , Y: 512)
ADMIN_EDIT_TABLE_CENTER_X = 681
ADMIN_EDIT_TABLE_CENTER_Y = 512
ADMIN_EDIT_TABLE_W_HALF = 100 # (ตั้งค่า W/H ประมาณ)
ADMIN_EDIT_TABLE_H_HALF = 40
ADMIN_EDIT_TABLE_BUTTON_REGION = {
    "x_start": ADMIN_EDIT_TABLE_CENTER_X - ADMIN_EDIT_TABLE_W_HALF, "x_end": ADMIN_EDIT_TABLE_CENTER_X + ADMIN_EDIT_TABLE_W_HALF,
    "y_start": ADMIN_EDIT_TABLE_CENTER_Y - ADMIN_EDIT_TABLE_H_HALF, "y_end": ADMIN_EDIT_TABLE_CENTER_Y + ADMIN_EDIT_TABLE_H_HALF
}

# 🟢 NEW: ปุ่ม "กลับไปหน้ารวม" (X: 472 , Y: 502)
ADMIN_BACK_TO_SUMMARY_CENTER_X = 472
ADMIN_BACK_TO_SUMMARY_CENTER_Y = 502
ADMIN_BACK_TO_SUMMARY_W_HALF = 100 # (ประมาณ)
ADMIN_BACK_TO_SUMMARY_H_HALF = 40 # (ประมาณ)
ADMIN_BACK_TO_SUMMARY_REGION = {
    "x_start": ADMIN_BACK_TO_SUMMARY_CENTER_X - ADMIN_BACK_TO_SUMMARY_W_HALF, "x_end": ADMIN_BACK_TO_SUMMARY_CENTER_X + ADMIN_BACK_TO_SUMMARY_W_HALF,
    "y_start": ADMIN_BACK_TO_SUMMARY_CENTER_Y - ADMIN_BACK_TO_SUMMARY_H_HALF, "y_end": ADMIN_BACK_TO_SUMMARY_CENTER_Y + ADMIN_BACK_TO_SUMMARY_H_HALF
}


# --- หมวดที่ 8: หน้าข้อมูลโปรไฟล์ (Profile Page) ---
PROF_L_COL_X = 318
PROF_R_COL_X = 706
PROF_BOX_W = 310
PROF_BOX_H = 55
PROF_LBL_H = 30
ORIG_PROFILE_USERNAME_LABEL = {"x": PROF_L_COL_X, "y": 269, "width": PROF_BOX_W, "height": PROF_LBL_H}
ORIG_PROFILE_USERNAME_DISPLAY = {"x": PROF_L_COL_X, "y": 300, "width": PROF_BOX_W, "height": PROF_BOX_H}
ORIG_PROFILE_PHONE_LABEL    = {"x": PROF_R_COL_X, "y": 269, "width": PROF_BOX_W, "height": PROF_LBL_H}
ORIG_PROFILE_PHONE_DISPLAY  = {"x": PROF_R_COL_X, "y": 300, "width": PROF_BOX_W, "height": PROF_BOX_H}

ORIG_PROFILE_PASSWORD_LABEL = {"x": PROF_L_COL_X, "y": 404, "width": PROF_BOX_W, "height": PROF_LBL_H}
ORIG_PROFILE_PASSWORD_DISPLAY = {"x": PROF_L_COL_X, "y": 435, "width": PROF_BOX_W, "height": PROF_BOX_H}

ORIG_PROFILE_EMAIL_LABEL    = {"x": PROF_R_COL_X, "y": 404, "width": PROF_BOX_W, "height": PROF_LBL_H}
ORIG_PROFILE_EMAIL_DISPLAY  = {"x": PROF_R_COL_X, "y": 435, "width": PROF_BOX_W, "height": PROF_BOX_H}

ORIG_PROFILE_IMAGE_BOX = {"x": 318, "y": 530, "width": 150, "height": 150} 

PROF_EDIT_CENTER_X = 974; PROF_EDIT_CENTER_Y = 191; PROF_EDIT_W_HALF = 70; PROF_EDIT_H_HALF = 30
PROFILE_EDIT_BUTTON_REGION = {
    "x_start": PROF_EDIT_CENTER_X - PROF_EDIT_W_HALF, "x_end": PROF_EDIT_CENTER_X + PROF_EDIT_W_HALF,
    "y_start": PROF_EDIT_CENTER_Y - PROF_EDIT_H_HALF, "y_end": PROF_EDIT_CENTER_Y + PROF_EDIT_H_HALF
}
PROF_CONFIRM_CENTER_X = 1164; PROF_CONFIRM_CENTER_Y = 191; PROF_CONFIRM_W_HALF = 70; PROF_CONFIRM_H_HALF = 30
PROFILE_CONFIRM_BUTTON_REGION = {
    "x_start": PROF_CONFIRM_CENTER_X - PROF_CONFIRM_W_HALF, "x_end": PROF_CONFIRM_CENTER_X + PROF_CONFIRM_W_HALF,
    "y_start": PROF_CONFIRM_CENTER_Y - PROF_CONFIRM_H_HALF, "y_end": PROF_CONFIRM_CENTER_Y + PROF_CONFIRM_H_HALF
}


# --- หมวดที่ 9: องค์ประกอบทั่วไปของหน้า (General Page Elements) ---
CART_ICON_REGION = {"x_start": 0, "x_end": 70, "y_start": 0, "y_end": 70} 
BACK_ICON_REGION = {"x_start": 20, "x_end": 90, "y_start": 20, "y_end": 90} 

CONFIRM_CENTER_X = 677
CONFIRM_CENTER_Y = 1008
CONFIRM_W_HALF = 140
CONFIRM_H_HALF = 40
CONFIRM_BUTTON_REGION = {
    "x_start": CONFIRM_CENTER_X - CONFIRM_W_HALF, "x_end": CONFIRM_CENTER_X + CONFIRM_W_HALF,
    "y_start": CONFIRM_CENTER_Y - CONFIRM_H_HALF, "y_end": CONFIRM_CENTER_Y + CONFIRM_H_HALF
}
DELETE_MENU_BUTTON = {"x_start": 890, "x_end": 1050, "y_start": 350, "y_end": 390}
ORIG_TEXTBOX_X = 320; ORIG_TEXTBOX_Y = 409; ORIG_TEXTBOX_W = 710; ORIG_TEXTBOX_H = 510

# ----------------------------------------------------------------------
# 🟢 START: (แก้ไข) หมวดที่ 10: หน้ารวม (Summary Page Specific)
# ----------------------------------------------------------------------
SUMMARY_ADD_ITEM_CENTER_X = 679
SUMMARY_ADD_ITEM_CENTER_Y = 347
SUMMARY_ADD_ITEM_W_HALF = 100
SUMMARY_ADD_ITEM_H_HALF = 40
SUMMARY_ADD_ITEM_REGION = {
    "x_start": SUMMARY_ADD_ITEM_CENTER_X - SUMMARY_ADD_ITEM_W_HALF, "x_end": SUMMARY_ADD_ITEM_CENTER_X + SUMMARY_ADD_ITEM_W_HALF,
    "y_start": SUMMARY_ADD_ITEM_CENTER_Y - SUMMARY_ADD_ITEM_H_HALF, "y_end": SUMMARY_ADD_ITEM_CENTER_Y + SUMMARY_ADD_ITEM_H_HALF
}

SUMMARY_ORDER_CENTER_X = 200
SUMMARY_ORDER_CENTER_Y = 348
SUMMARY_ORDER_W_HALF = 100 
SUMMARY_ORDER_H_HALF = 40 
SUMMARY_GOTO_ORDER_REGION = {
    "x_start": SUMMARY_ORDER_CENTER_X - SUMMARY_ORDER_W_HALF, "x_end": SUMMARY_ORDER_CENTER_X + SUMMARY_ORDER_W_HALF,
    "y_start": SUMMARY_ORDER_CENTER_Y - SUMMARY_ORDER_H_HALF, "y_end": SUMMARY_ORDER_CENTER_Y + SUMMARY_ORDER_H_HALF
}

# 🟢 NEW: ปุ่มไปหน้าเจ้าหน้าที่ (Admin Edit)
SUMMARY_ADMIN_EDIT_CENTER_X = 1153
SUMMARY_ADMIN_EDIT_CENTER_Y = 355
SUMMARY_ADMIN_EDIT_W_HALF = 100 # (ใช้ค่าประมาณ)
SUMMARY_ADMIN_EDIT_H_HALF = 40 # (ใช้ค่าประมาณ)
SUMMARY_ADMIN_EDIT_REGION = {
    "x_start": SUMMARY_ADMIN_EDIT_CENTER_X - SUMMARY_ADMIN_EDIT_W_HALF, "x_end": SUMMARY_ADMIN_EDIT_CENTER_X + SUMMARY_ADMIN_EDIT_W_HALF,
    "y_start": SUMMARY_ADMIN_EDIT_CENTER_Y - SUMMARY_ADMIN_EDIT_H_HALF, "y_end": SUMMARY_ADMIN_EDIT_CENTER_Y + SUMMARY_ADMIN_EDIT_H_HALF
}

# 🟢 NEW: ปุ่มไปหน้าเงิน
SUMMARY_MONEY_CENTER_X = 201
SUMMARY_MONEY_CENTER_Y = 486
SUMMARY_MONEY_W_HALF = 100 # (ใช้ค่าประมาณ)
SUMMARY_MONEY_H_HALF = 40 # (ใช้ค่าประมาณ)
SUMMARY_MONEY_PAGE_REGION = {
    "x_start": SUMMARY_MONEY_CENTER_X - SUMMARY_MONEY_W_HALF, "x_end": SUMMARY_MONEY_CENTER_X + SUMMARY_MONEY_W_HALF,
    "y_start": SUMMARY_MONEY_CENTER_Y - SUMMARY_MONEY_H_HALF, "y_end": SUMMARY_MONEY_CENTER_Y + SUMMARY_MONEY_H_HALF
}
# ----------------------------------------------------------------------
# 🟢 END: (แก้ไข)
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# 🟢 START: (แก้ไข) หน้าเงิน (Money Page Specific) - ใช้ปุ่มคลิก
# ----------------------------------------------------------------------
MONEY_PRICE_PER_PERSON = 10 # 🟢 (ราคา 10 บาทตามโค้ดเดิม)
MONEY_CLICK_W_HALF = 100 # (ขนาดปุ่มประมาณ)
MONEY_CLICK_H_HALF = 50  # (ขนาดปุ่มประมาณ)

# (1 คน)
MONEY_BTN_1_CENTER_X = 159; MONEY_BTN_1_CENTER_Y = 198
MONEY_BTN_1_REGION = {
    "x_start": MONEY_BTN_1_CENTER_X - MONEY_CLICK_W_HALF, "x_end": MONEY_BTN_1_CENTER_X + MONEY_CLICK_W_HALF,
    "y_start": MONEY_BTN_1_CENTER_Y - MONEY_CLICK_H_HALF, "y_end": MONEY_BTN_1_CENTER_Y + MONEY_CLICK_H_HALF
}
# (2 คน)
MONEY_BTN_2_CENTER_X = 490; MONEY_BTN_2_CENTER_Y = 197
MONEY_BTN_2_REGION = {
    "x_start": MONEY_BTN_2_CENTER_X - MONEY_CLICK_W_HALF, "x_end": MONEY_BTN_2_CENTER_X + MONEY_CLICK_W_HALF,
    "y_start": MONEY_BTN_2_CENTER_Y - MONEY_CLICK_H_HALF, "y_end": MONEY_BTN_2_CENTER_Y + MONEY_CLICK_H_HALF
}
# (3 คน)
MONEY_BTN_3_CENTER_X = 815; MONEY_BTN_3_CENTER_Y = 209
MONEY_BTN_3_REGION = {
    "x_start": MONEY_BTN_3_CENTER_X - MONEY_CLICK_W_HALF, "x_end": MONEY_BTN_3_CENTER_X + MONEY_CLICK_W_HALF,
    "y_start": MONEY_BTN_3_CENTER_Y - MONEY_CLICK_H_HALF, "y_end": MONEY_BTN_3_CENTER_Y + MONEY_CLICK_H_HALF
}
# (4 คน)
MONEY_BTN_4_CENTER_X = 158; MONEY_BTN_4_CENTER_Y = 397
MONEY_BTN_4_REGION = {
    "x_start": MONEY_BTN_4_CENTER_X - MONEY_CLICK_W_HALF, "x_end": MONEY_BTN_4_CENTER_X + MONEY_CLICK_W_HALF,
    "y_start": MONEY_BTN_4_CENTER_Y - MONEY_CLICK_H_HALF, "y_end": MONEY_BTN_4_CENTER_Y + MONEY_CLICK_H_HALF
}
# (5 คน)
MONEY_BTN_5_CENTER_X = 491; MONEY_BTN_5_CENTER_Y = 390
MONEY_BTN_5_REGION = {
    "x_start": MONEY_BTN_5_CENTER_X - MONEY_CLICK_W_HALF, "x_end": MONEY_BTN_5_CENTER_X + MONEY_CLICK_W_HALF,
    "y_start": MONEY_BTN_5_CENTER_Y - MONEY_CLICK_H_HALF, "y_end": MONEY_BTN_5_CENTER_Y + MONEY_CLICK_H_HALF
}
# (6 คน)
MONEY_BTN_6_CENTER_X = 825; MONEY_BTN_6_CENTER_Y = 397
MONEY_BTN_6_REGION = {
    "x_start": MONEY_BTN_6_CENTER_X - MONEY_CLICK_W_HALF, "x_end": MONEY_BTN_6_CENTER_X + MONEY_CLICK_W_HALF,
    "y_start": MONEY_BTN_6_CENTER_Y - MONEY_CLICK_H_HALF, "y_end": MONEY_BTN_6_CENTER_Y + MONEY_CLICK_H_HALF
}
# (กำหนดเอง)
MONEY_BTN_CUSTOM_CENTER_X = 152; MONEY_BTN_CUSTOM_CENTER_Y = 578
MONEY_BTN_CUSTOM_REGION = {
    "x_start": MONEY_BTN_CUSTOM_CENTER_X - MONEY_CLICK_W_HALF, "x_end": MONEY_BTN_CUSTOM_CENTER_X + MONEY_CLICK_W_HALF,
    "y_start": MONEY_BTN_CUSTOM_CENTER_Y - MONEY_CLICK_H_HALF, "y_end": MONEY_BTN_CUSTOM_CENTER_Y + MONEY_CLICK_H_HALF
}
# ----------------------------------------------------------------------
# 🟢 END: (แก้ไข)
# ----------------------------------------------------------------------

# ----------------------------------------------------------------------
# 🟢 START: (เพิ่ม) หน้าบิล (Bill Page Specific) - พิกัด Layout
# ----------------------------------------------------------------------
# (พิกัดอ้างอิงจากโลโก้ Mooay Noi ที่อยู่ด้านบน)
BILL_CENTER_X = 1366 // 2 # (683)
BILL_CONTENT_WIDTH = 600
BILL_CONTENT_START_X = BILL_CENTER_X - (BILL_CONTENT_WIDTH // 2) # (383)

# (Header)
ORIG_BILL_HEADER_L1 = {"x": BILL_CONTENT_START_X, "y": 360, "width": BILL_CONTENT_WIDTH, "height": 40} # ชื่อร้าน
ORIG_BILL_HEADER_L2 = {"x": BILL_CONTENT_START_X, "y": 400, "width": BILL_CONTENT_WIDTH, "height": 25} # ที่อยู่ 1
ORIG_BILL_HEADER_L3 = {"x": BILL_CONTENT_START_X, "y": 425, "width": BILL_CONTENT_WIDTH, "height": 25} # ที่อยู่ 2
ORIG_BILL_HEADER_L4 = {"x": BILL_CONTENT_START_X, "y": 450, "width": BILL_CONTENT_WIDTH, "height": 25} # โทร/Tax
# (Divider)
ORIG_BILL_DIVIDER1  = {"x": BILL_CONTENT_START_X, "y": 485, "width": BILL_CONTENT_WIDTH, "height": 20}
# (Info)
ORIG_BILL_INFO_L1   = {"x": BILL_CONTENT_START_X, "y": 505, "width": BILL_CONTENT_WIDTH, "height": 25} # โต๊ะ / วันที่
ORIG_BILL_DIVIDER2  = {"x": BILL_CONTENT_START_X, "y": 530, "width": BILL_CONTENT_WIDTH, "height": 20}
# (Body)
ORIG_BILL_BODY_HEADER = {"x": BILL_CONTENT_START_X, "y": 550, "width": BILL_CONTENT_WIDTH, "height": 25} # หัวข้อ (รายการ/ราคา)
ORIG_BILL_BODY_ITEM   = {"x": BILL_CONTENT_START_X, "y": 580, "width": BILL_CONTENT_WIDTH, "height": 30} # รายการ
ORIG_BILL_DIVIDER3  = {"x": BILL_CONTENT_START_X, "y": 615, "width": BILL_CONTENT_WIDTH, "height": 20}
# (Footer Total)
ORIG_BILL_SUBTOTAL  = {"x": BILL_CONTENT_START_X, "y": 640, "width": BILL_CONTENT_WIDTH, "height": 25} # ราคารวม
ORIG_BILL_VAT       = {"x": BILL_CONTENT_START_X, "y": 665, "width": BILL_CONTENT_WIDTH, "height": 25} # VAT
ORIG_BILL_TOTAL     = {"x": BILL_CONTENT_START_X, "y": 695, "width": BILL_CONTENT_WIDTH, "height": 40} # ยอดสุทธิ
# (Footer Message)
ORIG_BILL_FOOTER1   = {"x": BILL_CONTENT_START_X, "y": 740, "width": BILL_CONTENT_WIDTH, "height": 25} # (ชำระแล้ว)
ORIG_BILL_FOOTER2   = {"x": BILL_CONTENT_START_X, "y": 765, "width": BILL_CONTENT_WIDTH, "height": 25} # (ขอบคุณ)
# ----------------------------------------------------------------------
# 🟢 END: (เพิ่ม)
# ----------------------------------------------------------------------


# --- หมวดที่ 11: หน้าเมนูอาหาร (Food Menu Specific) ---
MENU_SUB_FRAME_REGION = {"x_start": 230, "y_start": 607, "x_end": 1146, "y_end": 3802} 

ANCHOR_BUTTONS = [
    {"center_x": 312, "center_y": 454, "target_y": 657, "region_name": "เนื้อ"}, 
    {"center_x": 501, "center_y": 455, "target_y": 1445, "region_name": "อาหารทะเล"},
    {"center_x": 694, "center_y": 450, "target_y": 2223, "region_name": "ผักผลไม้"},
    {"center_x": 874, "center_y": 457, "target_y": 2998, "region_name": "ของทานเล่น"},
    {"center_x": 1096, "center_y": 455, "target_y": 3455, "region_name": "ของหวาน"},
]
ANCHOR_CLICK_WIDTH = 160; ANCHOR_CLICK_HEIGHT = 80
anchor_half_w = ANCHOR_CLICK_WIDTH // 2; anchor_half_h = ANCHOR_CLICK_HEIGHT // 2
ANCHOR_REGIONS = [{"x_start": btn["center_x"] - anchor_half_w, "x_end": btn["center_x"] + anchor_half_w,
                   "y_start": btn["center_y"] - anchor_half_h, "y_end": btn["center_y"] + anchor_half_h,
                   "target_y": btn["target_y"], "region_name": btn["region_name"]} for btn in ANCHOR_BUTTONS]

MENU_DATA = [
    {"category": "เนื้อ", "name": "เนื้อสันนอก", "image": "เนื้อสันนอก.png", "description": "", "price": 120},
    {"category": "เนื้อ", "name": "เนื้อสันใน", "image": "เนื้อสันใน.png", "description": "", "price": 150},
    {"category": "เนื้อ", "name": "เนื้อสันคอ", "image": "เนื้อสันคอ.png", "description": "", "price": 130},
    {"category": "เนื้อ", "name": "ลิ้นวัว", "image": "ลิ้นวัว.png", "description": "", "price": 180},
    {"category": "เนื้อ", "name": "สามชั้น", "image": "สามชั้น.png", "description": "", "price": 100},
    {"category": "เนื้อ", "name": "สันคอหมู", "image": "สันคอหมู.png", "description": "", "price": 90},
    {"category": "เนื้อ", "name": "สันนอกหมู", "image": "สันนอกหมู.png", "description": "", "price": 85},
    {"category": "เนื้อ", "name": "สันในหมู", "image": "สันในหมู.png", "description": "", "price": 95},
    
    {"category": "อาหารทะเล", "name": "หมึกกระดอง", "image": "หมึกกระดอง.png", "description": "", "price": 80},
    {"category": "อาหารทะเล", "name": "กุ้งแม่น้ำ", "image": "กุ้งแม่น้ำ.png", "description": "", "price": 200},
    {"category": "อาหารทะเล", "name": "แซลม่อน", "image": "แซลม่อน.png", "description": "", "price": 160},
    {"category": "อาหารทะเล", "name": "หอยแมลงภู่", "image": "หอยแมลงภู่.png", "description": "", "price": 70},
    {"category": "อาหารทะเล", "name": "หอยเชลล์", "image": "หอยเชลล์.png", "description": "", "price": 110},
    {"category": "อาหารทะเล", "name": "หอยปีกนก", "image": "หอยปีกนก.png", "description": "", "price": 100},
    {"category": "อาหารทะเล", "name": "ทูน่า", "image": "ทูน่า.png", "description": "", "price": 140},
    {"category": "อาหารทะเล", "name": "อูนิ", "image": "อูนิ.png", "description": "", "price": 300},

    {"category": "ผักผลไม้", "name": "กวางตุ้ง", "image": "กวางตุ้ง.png", "description": "", "price": 30},
    {"category": "ผักผลไม้", "name": "กะหล่ำ", "image": "กะหล่ำ.png", "description": "", "price": 25},
    {"category": "ผักผลไม้", "name": "ข้าวโพด", "image": "ข้าวโพด.png", "description": "", "price": 35},
    {"category": "ผักผลไม้", "name": "เห็ดเข็มทอง", "image": "เห็ดเข็มทอง.png", "description": "", "price": 40},
    {"category": "ผักผลไม้", "name": "ฟักทอง", "image": "ฟักทอง.png", "description": "", "price": 30},
    {"category": "ผักผลไม้", "name": "แครอท", "image": "แครอท.png", "description": "", "price": 25},
    {"category": "ผักผลไม้", "name": "เห็ดออรินจิ", "image": "เห็ดออรินจิ.png", "description": "", "price": 45},
    {"category": "ผักผลไม้", "name": "หัวหอม", "image": "หัวหอม.png", "description": "", "price": 20},

    {"category": "ของทานเล่น", "name": "เฟรนซ์ฟรายส์", "image": "เฟรนซ์ฟรายส์.png", "description": "", "price": 60},
    {"category": "ของทานเล่น", "name": "ชีสบอล", "image": "ชีสบอล.png", "description": "", "price": 70},
    {"category": "ของทานเล่น", "name": "ไก่ทอด", "image": "ไก่ทอด.png", "description": "", "price": 80},
    {"category": "ของทานเล่น", "name": "หอมทอด", "image": "หอมทอด.png", "description": "", "price": 65},

    {"category": "ของหวาน", "name": "ไอศกรีมวนิลา", "image": "ไอศกรีมวนิลา.png", "description": "", "price": 50},
    {"category": "ของหวาน", "name": "ไอศกรีมสตรอเบอร์รี่", "image": "ไอศกรีมสตรอเบอร์รี่.png", "description": "", "price": 50},
    {"category": "ของหวาน", "name": "ไอศกรีมช็อกโกแลต", "image": "ไอศกรีมช็อกโกแลต.png", "description": "", "price": 50},
    {"category": "ของหวาน", "name": "ไอศกรีมนมสด", "image": "ไอศกรีมนมสด.png", "description": "", "price": 55},
]
FOOD_ITEM_IMAGE_WIDTH = 120 
FOOD_ITEM_IMAGE_HEIGHT = 100 

FOOD_ITEMS_LIST = [item['name'] for item in MENU_DATA]
FOOD_CLICK_WIDTH = 140; FOOD_CLICK_HEIGHT = 100
food_half_w = FOOD_CLICK_WIDTH // 2; food_half_h = FOOD_CLICK_HEIGHT // 2

ORIG_MENU_TABLE_LABEL = {"x": 1242, "y": 120, "width": 100, "height": 40}

MENU_BACK_TO_TABLE_CENTER_X = 1289
MENU_BACK_TO_TABLE_CENTER_Y = 220
MENU_BACK_TO_TABLE_W_HALF = 50
MENU_BACK_TO_TABLE_H_HALF = 20
MENU_BACK_TO_TABLE_REGION = {
    "x_start": MENU_BACK_TO_TABLE_CENTER_X - MENU_BACK_TO_TABLE_W_HALF, "x_end": MENU_BACK_TO_TABLE_CENTER_X + MENU_BACK_TO_TABLE_W_HALF,
    "y_start": MENU_BACK_TO_TABLE_CENTER_Y - MENU_BACK_TO_TABLE_H_HALF, "y_end": MENU_BACK_TO_TABLE_CENTER_Y + MENU_BACK_TO_TABLE_H_HALF
}

# --- หมวดที่ 12: หน้าตารางโต๊ะ (Table Page Specific) ---
TABLE_CENTERS = [
    {"x": 407, "y": 646},{"x": 247, "y": 637},{"x": 55, "y": 636}, {"x": 76, "y": 496},{"x": 73, "y": 369},
    {"x": 69, "y": 233},{"x": 76, "y": 91},{"x": 248, "y": 73},{"x": 419, "y": 77},{"x": 421, "y": 226},
    {"x": 414, "y": 357},{"x": 601, "y": 365}, {"x": 787, "y": 365}, {"x": 945, "y": 365}, {"x": 945, "y": 225}, 
    {"x": 945, "y": 75}, {"x": 1118, "y": 75}, {"x": 1285, "y": 75}, {"x": 1285, "y": 225}, {"x": 1285, "y": 365},
    {"x": 1285, "y": 500}, {"x": 1285, "y": 640}, {"x": 1118, "y": 640}, {"x": 945, "y": 640}
]
TABLE_CLICK_WIDTH = 100; TABLE_CLICK_HEIGHT = 100
table_half_w = TABLE_CLICK_WIDTH // 2; table_half_h = TABLE_CLICK_HEIGHT // 2
TABLE_REGIONS = [{"name": f"โต๊ะ {i + 1}", "x_start": center["x"] - table_half_w, "x_end": center["x"] + table_half_w,
                  "y_start": center["y"] - table_half_h, "y_end": center["y"] + table_half_h,
                  "center_x": center["x"], "center_y": center["y"]} for i, center in enumerate(TABLE_CENTERS)]

TABLE_ALIGNMENT_CENTERS = [
    {"x": 415, "y": 640}, {"x": 248, "y": 640}, {"x": 70, "y": 640}, {"x": 70, "y": 500}, {"x": 70, "y": 365},
    {"x": 70, "y": 225}, {"x": 70, "y": 75}, {"x": 248, "y": 75}, {"x": 415, "y": 75}, {"x": 415, "y": 225},
    {"x": 415, "y": 365}, {"x": 601, "y": 365}, {"x": 787, "y": 365}, {"x": 945, "y": 365}, {"x": 945, "y": 225},
    {"x": 945, "y": 75}, {"x": 1118, "y": 75}, {"x": 1285, "y": 75}, {"x": 1285, "y": 225}, {"x": 1285, "y": 365},
    {"x": 1285, "y": 500}, {"x": 1285, "y": 640}, {"x": 1118, "y": 640}, {"x": 945, "y": 640}
]


# ----------------------------------------------------------------------
# 🟢 START: (แก้ไข) ลบ "ราคา" ออกจากหน้าเพิ่ม
# ----------------------------------------------------------------------
# --- หมวดที่ 13: หน้าเพิ่มสินค้า (Add Item Page) ---
ADD_ITEM_CENTER_X = 1366 // 2 # (683)
ORIG_ADD_ITEM_IMAGE_BOX = {"x": ADD_ITEM_CENTER_X-100, "y": 250, "width": 200, "height": 150} 
ORIG_ADD_ITEM_NAME_LABEL = {"x": ADD_ITEM_CENTER_X-150, "y": 420, "width": 100, "height": 30} 
ORIG_ADD_ITEM_NAME_BOX = {"x": ADD_ITEM_CENTER_X-150, "y": 455, "width": 300, "height": 50} 
ORIG_ADD_ITEM_CAT_LABEL = {"x": ADD_ITEM_CENTER_X-150, "y": 510, "width": 100, "height": 30} 
ORIG_ADD_ITEM_CAT_BOX = {"x": ADD_ITEM_CENTER_X-150, "y": 545, "width": 300, "height": 50} 
# (ลบช่องราคา)

ADD_ITEM_CONFIRM_CENTER_X = 1205
ADD_ITEM_CONFIRM_CENTER_Y = 635
ADD_ITEM_CONFIRM_W_HALF = 70 
ADD_ITEM_CONFIRM_H_HALF = 30 
ADD_ITEM_CONFIRM_REGION = {
    "x_start": ADD_ITEM_CONFIRM_CENTER_X - ADD_ITEM_CONFIRM_W_HALF, "x_end": ADD_ITEM_CONFIRM_CENTER_X + ADD_ITEM_CONFIRM_W_HALF,
    "y_start": ADD_ITEM_CONFIRM_CENTER_Y - ADD_ITEM_CONFIRM_H_HALF, "y_end": ADD_ITEM_CONFIRM_CENTER_Y + ADD_ITEM_CONFIRM_H_HALF
}

# 🟢 NEW: ปุ่มยืนยันอันใหม่ (X: 1200 , Y: 638)
ADD_ITEM_CONFIRM_NEW_CENTER_X = 1200
ADD_ITEM_CONFIRM_NEW_CENTER_Y = 638
ADD_ITEM_CONFIRM_NEW_W_HALF = 70 
ADD_ITEM_CONFIRM_NEW_H_HALF = 30 
ADD_ITEM_CONFIRM_REGION_NEW = {
    "x_start": ADD_ITEM_CONFIRM_NEW_CENTER_X - ADD_ITEM_CONFIRM_NEW_W_HALF, "x_end": ADD_ITEM_CONFIRM_NEW_CENTER_X + ADD_ITEM_CONFIRM_NEW_W_HALF,
    "y_start": ADD_ITEM_CONFIRM_NEW_CENTER_Y - ADD_ITEM_CONFIRM_NEW_H_HALF, "y_end": ADD_ITEM_CONFIRM_NEW_CENTER_Y + ADD_ITEM_CONFIRM_NEW_H_HALF
}

DELETE_ITEM_CENTER_X = 1044
DELETE_ITEM_CENTER_Y = 640
DELETE_ITEM_W_HALF = 70 
DELETE_ITEM_H_HALF = 30 
DELETE_ITEM_BUTTON_REGION = {
    "x_start": DELETE_ITEM_CENTER_X - DELETE_ITEM_W_HALF, "x_end": DELETE_ITEM_CENTER_X + DELETE_ITEM_W_HALF,
    "y_start": DELETE_ITEM_CENTER_Y - DELETE_ITEM_H_HALF, "y_end": DELETE_ITEM_CENTER_Y + DELETE_ITEM_H_HALF
}
# ----------------------------------------------------------------------
# 🟢 END: (แก้ไข)
# ----------------------------------------------------------------------

# --- หมวดที่ 14: หน้า Order Status (พิกัด Text) ---
ORIG_ORDER_STATUS_BOX = {"x": 100, "y": 200, "width": 1166, "height": 550}

# --- จบหมวดการตั้งค่าและค่าคงที่ ---


class ShabuApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Shabu Shabu Order System - All Clickable")
        self.geometry(WINDOW_SIZE)
        self.configure(bg="#F0F0F0")

        self.cart = defaultdict(int)
        self.current_page = "table_page"

        # Input Variables
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.reg_username_var = tk.StringVar()
        self.reg_password1_var = tk.StringVar()
        self.reg_password2_var = tk.StringVar()
        self.reg_phone_var = tk.StringVar()
        self.reg_email_var = tk.StringVar()
        self.forgot_email_var = tk.StringVar()
        self.forgot_phone_var = tk.StringVar()
        self.admin_username_var = tk.StringVar()
        self.admin_password_var = tk.StringVar()
        self.add_item_name_var = tk.StringVar()
        
        self.add_item_category_var = tk.StringVar()
        self.add_item_category_var.set(CATEGORY_OPTIONS[0]) 
        # (ลบ Price Var)
        
        # 🟢 (เพิ่ม) ตัวแปรสำหรับส่งค่าไปหน้าบิล
        self.final_bill_amount = 0 # (ยอดรวมที่คำนวณแล้ว)
        self.final_bill_person_count = 0 # (จำนวนคน)

        # 🟢 (เพิ่ม) ตัวแปรสำหรับแสดงผลบนหน้าบิล
        self.bill_header_l1_var = tk.StringVar()
        self.bill_header_l2_var = tk.StringVar()
        self.bill_header_l3_var = tk.StringVar()
        self.bill_header_l4_var = tk.StringVar()
        self.bill_divider_var = tk.StringVar(value="-"*60) # (เส้นคั่น)
        self.bill_info_l1_var = tk.StringVar()
        self.bill_body_header_var = tk.StringVar()
        self.bill_body_item_var = tk.StringVar()
        self.bill_subtotal_var = tk.StringVar()
        self.bill_vat_var = tk.StringVar()
        self.bill_total_var = tk.StringVar()
        self.bill_footer1_var = tk.StringVar()
        self.bill_footer2_var = tk.StringVar()

        # 🟢 (เพิ่ม) ตัวแปรสำหรับหน้าแก้
        self.fix_username_var = tk.StringVar()
        self.fix_password_var = tk.StringVar()

        # Display Variables
        self.profile_display_username = tk.StringVar()
        self.profile_display_phone = tk.StringVar()
        self.profile_display_email = tk.StringVar()
        self.profile_display_password = tk.StringVar() 

        # Original Images (PIL format)
        self.original_table_page_image = None
        self.original_login_image = None
        self.original_food_menu_image = None
        self.original_order_list_image = None
        self.original_summary_page_image = None 
        self.original_register_image = None
        self.original_forgot_image = None
        self.original_admin_edit_image = None
        self.original_profile_page_image = None
        self.original_add_item_page_image = None
        self.original_placeholder_image = None
        self.original_order_status_page_image = None 
        self.original_money_page_image = None # 🟢 NEW (เผื่อมีรูป)
        self.original_bill_page_image = None # 🟢 NEW (เพิ่ม)
        self.original_fix_page_image = None # 🟢 NEW (เพิ่ม)

        # Tkinter Image References
        self.table_bg_image_tk = None
        self.login_bg_image_tk = None
        self.food_menu_bg_image_tk = None
        self.order_list_bg_image_tk = None
        self.summary_bg_image_tk = None
        self.register_bg_image_tk = None
        self.forgot_bg_image_tk = None
        self.admin_edit_bg_image_tk = None
        self.profile_page_bg_image_tk = None
        self.add_item_bg_image_tk = None
        self.reg_profile_preview_tk = None
        self.menu_profile_image_tk = None
        self.profile_page_image_tk = None
        self.add_item_image_preview_tk = None
        self.placeholder_image_tk = None
        self.order_status_bg_image_tk = None 
        self.money_page_bg_image_tk = None # 🟢 NEW
        self.bill_page_bg_image_tk = None # 🟢 NEW (เพิ่ม)
        self.fix_page_bg_image_tk = None # 🟢 NEW (เพิ่ม)
        self.qr_photo_tk = None # 🟢 NEW (สำหรับ Pop-up)
        
        self.sub_canvas = None 
        self.menu_items_frame = None
        self.menu_image_references = [] 

        # State Variables
        self.content_frame = tk.Frame(self, bg="#F0F0F0")
        self.current_scale_factor = 1.0
        self.selected_profile_image_path = None
        self.current_user_profile_path = None
        self.lookup_user_data = {}
        self.selected_table_index = None
        self.current_table_name_var = tk.StringVar()
        self.add_item_image_path = None
        self.profile_edit_mode = tk.BooleanVar(value=False) 

        # Table Status
        self.table_status = ['available'] * len(TABLE_CENTERS)
        self.table_status_labels_table_page = []
        self.table_status_labels_admin_page = [] # 🟢 NEW

        # Initialization
        if not self.check_file_paths(): self.quit(); return
        self.load_original_images()
        self.init_database()
        self.create_widgets()
        self.show_page(self.current_page)

    def get_click_position(self, event):
        scale = self.current_scale_factor
        if scale == 0: return

        orig_x = event.x / scale
        orig_y = event.y / scale

        print(f"X: {int(orig_x)} , Y: {int(orig_y)}")

        self.check_click(orig_x, orig_y)

    def check_file_paths(self):
        all_ok = True
        for name, path in IMAGE_PATHS.items():
            # 🟢 NEW: (แก้ไข) อนุญาตให้ไฟล์หน้าเงิน, หน้าบิล หายไปได้
            if name in ["money_page_bg", "bill_page_bg"] and not os.path.exists(path): # 🟢 (แก้ไข)
                print(f"🟠 WARNING: Optional file '{os.path.basename(path)}' not found. Will use gray background.") # 🟢 (แก้ไข)
                continue # ข้ามไปไฟล์ถัดไป
                
            # 🟢 (เพิ่ม) อนุญาตให้ไฟล์หน้าแก้หายไปได้
            if name == "fix_page_bg" and not os.path.exists(path):
                print(f"🟠 WARNING: Optional file 'หน้าแก้.png' not found. Will use gray background.")
                continue # ข้ามไปไฟล์ถัดไป
                
            if not os.path.exists(path):
                error_message = f"❌ Missing Image File:\n'{name}' expected at:\n{path}"
                messagebox.showerror("Fatal Error: Missing File", error_message)
                all_ok = False
        return all_ok

    def load_original_images(self):
        try:
            for name, path in IMAGE_PATHS.items():
                if os.path.exists(path): # 🟢 NEW: เช็คว่าไฟล์มีจริงก่อนโหลด
                    attr_name = f"original_{name.replace('_bg', '_image')}"
                    setattr(self, attr_name, Image.open(path))
            print("✅ Original images loaded successfully.")
        except Exception as e:
            messagebox.showerror("Error Loading Images", f"Failed to load images: {e}")
            self.quit()

    def init_database(self):
        try:
            os.makedirs(PROFILE_DIR, exist_ok=True)
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            # --- ตาราง Users (เหมือนเดิม) ---
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL, password TEXT NOT NULL, role TEXT NOT NULL DEFAULT 'user',
                profile_image_path TEXT, phone TEXT, email TEXT );
            """)
            cursor.execute("PRAGMA table_info(users)")
            columns = [col[1] for col in cursor.fetchall()]
            if 'profile_image_path' not in columns: cursor.execute("ALTER TABLE users ADD COLUMN profile_image_path TEXT")
            if 'phone' not in columns: cursor.execute("ALTER TABLE users ADD COLUMN phone TEXT")
            if 'email' not in columns: cursor.execute("ALTER TABLE users ADD COLUMN email TEXT")

            staff_username = 'staff'; staff_password = 'ShabuStaff99'; staff_role = 'staff'
            staff_profile_db_value = os.path.join(PROFILE_DIR, "staff")
            cursor.execute("INSERT OR IGNORE INTO users (username, password, role, profile_image_path) VALUES (?, ?, ?, ?)",
                           (staff_username, staff_password, staff_role, staff_profile_db_value))
            cursor.execute("UPDATE users SET password = ?, profile_image_path = ? WHERE username = ?",
                           (staff_password, staff_profile_db_value, staff_username))

            # --- ตาราง Orders (อัปเกรด) ---
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Orders (
                order_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                table_name TEXT, 
                order_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                status TEXT DEFAULT 'pending'
            );""")
            
            cursor.execute("PRAGMA table_info(Orders)")
            order_columns = [col[1] for col in cursor.fetchall()]
            if 'table_name' not in order_columns: 
                cursor.execute("ALTER TABLE Orders ADD COLUMN table_name TEXT")
            if 'status' not in order_columns: 
                cursor.execute("ALTER TABLE Orders ADD COLUMN status TEXT DEFAULT 'pending'")

            # --- ตาราง Menu (เหมือนเดิม) ---
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS Menu ( 
                item_id INTEGER PRIMARY KEY AUTOINCREMENT, 
                order_id INTEGER,
                item_name TEXT NOT NULL, 
                quantity INTEGER NOT NULL, 
                FOREIGN KEY(order_id) REFERENCES Orders(order_id) 
            );""")

            conn.commit()
            conn.close()
            print(f"✅ Database initialized successfully at:\n{DATABASE_PATH}")
        except Exception as e:
            print(f"🔴 ERROR in init_database: {e}")
            messagebox.showerror("Database Error", f"Could not initialize database:\n{e}")
            self.quit()

    def create_widgets(self):
        self.content_frame.pack(fill='both', expand=True)

    def clear_content_frame(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def show_page(self, page_name):
        print(f"\n🔄 --- Switching to page: {page_name} ---")
        self.current_page = page_name

        if page_name not in ["login", "table_page"]:
                                  self.username_var.set(""); self.password_var.set("")
        if page_name != "register_page":
            self.reg_username_var.set(""); self.reg_password1_var.set(""); self.reg_password2_var.set("")
            self.reg_phone_var.set(""); self.reg_email_var.set("")
            self.selected_profile_image_path = None; self.reg_profile_preview_tk = None
        if page_name != "forgot_page":
            self.forgot_email_var.set(""); self.forgot_phone_var.set("")
        if page_name != "admin_edit_page":
            self.admin_username_var.set(""); self.admin_password_var.set("")
            
        if page_name != "profile_page":
                                  self.profile_display_username.set(""); self.profile_display_phone.set(""); self.profile_display_email.set("")
                                  self.profile_display_password.set("") 
                                  self.lookup_user_data = {}; self.profile_page_image_tk = None
                                  self.profile_edit_mode.set(False) 
                                  
        if page_name != "add_item_page":
            self.add_item_name_var.set("")
            self.add_item_category_var.set(CATEGORY_OPTIONS[0]) 
            # (ลบ Price Var)
            self.add_item_image_path = None; self.add_item_image_preview_tk = None

        if page_name == "table_page":
            self.current_user_profile_path = None; self.menu_profile_image_tk = None
            self.selected_table_index = None
            if self.cart: self.cart.clear(); print("🛒 Cart cleared.")
            if hasattr(self, 'current_table_name_var'): self.current_table_name_var.set("")
            
        if page_name != "order_status_page":
            pass 
            
        if page_name != "money_page":
            pass # (หน้าเงินไม่จำเป็นต้องล้างค่าแล้ว)
            
        # 🟢 NEW: (เพิ่ม)
        if page_name != "bill_page":
            self.final_bill_amount = 0
            self.final_bill_person_count = 0
            
        # 🟢 (เพิ่ม) ล้างค่าตัวแปรของหน้าแก้
        if page_name != "fix_page":
            self.fix_username_var.set("")
            self.fix_password_var.set("")
            pass

        self.clear_content_frame()

        page_methods = {
            "table_page": self.show_table_page, "login": self.show_login_page,
            "food_menu": self.show_food_menu, "order_list": self.show_order_list_screen,
            "summary_page": self.show_summary_page,
            "register_page": self.show_register_page,
            "forgot_page": self.show_forgot_page, "admin_edit_page": self.show_admin_edit_page,
            "profile_page": self.show_profile_page,
            "add_item_page": self.show_add_item_page,
            "order_status_page": self.show_order_status_page, 
            "money_page": self.show_money_page, # 🟢 NEW
            "bill_page": self.show_bill_page, # 🟢 NEW (เพิ่ม)
            "fix_page": self.show_fix_page, # 🟢 NEW
        }
        show_method = page_methods.get(page_name)
        if show_method: show_method()
        else:
            print(f"🔴 ERROR: Unknown page name '{page_name}'")
            messagebox.showerror("Navigation Error", f"Page '{page_name}' not found.")
            self.show_page("table_page")

    def manage_table_status(self):
        table_num = simpledialog.askinteger("จัดการสถานะโต๊ะ (1/2)", f"กรุณากรอกหมายเลขโต๊ะ (1-{len(TABLE_CENTERS)}):",
                                        parent=self, minvalue=1, maxvalue=len(TABLE_CENTERS))
        if table_num is None: return
        table_index = table_num - 1
        action = messagebox.askyesnocancel("จัดการสถานะโต๊ะ (2/2)", f"จัดการสถานะโต๊ะ {table_num}:\n\n"
                                       f" • กด 'Yes' = ตั้งเป็นโต๊ะเต็ม\n • กด 'No'  = ตั้งเป็นโต๊ะว่าง\n\n(กด 'Cancel' เพื่อยกเลิก)",
                                       parent=self, icon='question')
        new_status = 'occupied' if action is True else 'available' if action is False else None
        if new_status and self.table_status[table_index] != new_status:
            self.table_status[table_index] = new_status
            print(f"Table {table_num} status set to: {new_status}")
        elif new_status: print(f"Table {table_num} status already '{new_status}'. No change.")

    def check_click(self, orig_x, orig_y):
        page = self.current_page

        if page == "table_page":
            for i, region in enumerate(TABLE_REGIONS):
                if region["x_start"] <= orig_x <= region["x_end"] and region["y_start"] <= orig_y <= region["y_end"]:
                    if self.table_status[i] == 'occupied':
                        messagebox.showwarning("โต๊ะไม่ว่าง", f"{region['name']} นี้มีลูกค้าแล้ว\nกรุณาเลือกโต๊ะอื่น")
                    elif messagebox.askyesno("ยืนยันการเลือกโต๊ะ", f"เลือก {region['name']} ใช่หรือไม่?"):
                        self.selected_table_index = i
                        self.current_table_name_var.set(region['name'])
                        self.show_page("login")
                    return

        elif page == "login":
            # 🟢 (แก้ไข) ปุ่มลัดไปหน้า "แก้" (X: 678 , Y: 641)
            if LOGIN_GOTO_ADMIN_REGION["x_start"] <= orig_x <= LOGIN_GOTO_ADMIN_REGION["x_end"] and \
               LOGIN_GOTO_ADMIN_REGION["y_start"] <= orig_y <= LOGIN_GOTO_ADMIN_REGION["y_end"]:
                print("Shortcut to Fix Page") # 🟢 (แก้ไข)
                self.show_page("fix_page"); return # 🟢 (แก้ไข)
            
            if ADMIN_EDIT_BUTTON_REGION["x_start"] <= orig_x <= ADMIN_EDIT_BUTTON_REGION["x_end"] and \
               ADMIN_EDIT_BUTTON_REGION["y_start"] <= orig_y <= ADMIN_EDIT_BUTTON_REGION["y_end"]:
                self.show_page("admin_edit_page"); return
            
            if REGISTER_BUTTON_REGION["x_start"] <= orig_x <= REGISTER_BUTTON_REGION["x_end"] and \
               REGISTER_BUTTON_REGION["y_start"] <= orig_y <= REGISTER_BUTTON_REGION["y_end"]:
                self.show_page("register_page"); return
            
            if FORGOT_BUTTON_REGION["x_start"] <= orig_x <= FORGOT_BUTTON_REGION["x_end"] and \
               FORGOT_BUTTON_REGION["y_start"] <= orig_y <= FORGOT_BUTTON_REGION["y_end"]:
                self.show_page("forgot_page"); return
            if NEW_LOGIN_BUTTON_REGION["x_start"] <= orig_x <= NEW_LOGIN_BUTTON_REGION["x_end"] and \
               NEW_LOGIN_BUTTON_REGION["y_start"] <= orig_y <= NEW_LOGIN_BUTTON_REGION["y_end"]:
                self.validate_login(self.username_var.get(), self.password_var.get()); return
            if LOGIN_BUTTON_REGION["x_start"] <= orig_x <= LOGIN_BUTTON_REGION["x_end"] and \
               LOGIN_BUTTON_REGION["y_start"] <= orig_y <= LOGIN_BUTTON_REGION["y_end"]:
                self.validate_login(self.username_var.get(), self.password_var.get()); return
        
        elif page == "food_menu":
            
            if MENU_BACK_TO_TABLE_REGION["x_start"] <= orig_x <= MENU_BACK_TO_TABLE_REGION["x_end"] and \
               MENU_BACK_TO_TABLE_REGION["y_start"] <= orig_y <= MENU_BACK_TO_TABLE_REGION["y_end"]:
                self.show_page("table_page"); return
            
            if CART_ICON_REGION["x_start"] <= orig_x <= CART_ICON_REGION["x_end"] and \
               CART_ICON_REGION["y_start"] <= orig_y <= CART_ICON_REGION["y_end"]:
                self.show_page("order_list"); return
            
            for region in ANCHOR_REGIONS:
                if region["x_start"] <= orig_x <= region["x_end"] and region["y_start"] <= orig_y <= region["y_end"]:
                    self.scroll_menu_to_y(region['target_y']); return
            
            profile_box = ORIG_MENU_PROFILE_BOX
            if profile_box["x"] <= orig_x <= (profile_box["x"] + profile_box["width"]) and \
               profile_box["y"] <= orig_y <= (profile_box["y"] + profile_box["height"]):
                
                if self.lookup_user_data: 
                    self.show_page("profile_page")
                elif self.current_user_profile_path: 
                    print("User clicking their own profile. Looking up data...")
                    self.lookup_user_data_by_username(self.username_var.get())
                    self.show_page("profile_page")
                else:
                    print("No user data found to show profile.")
                return
                                
        elif page == "order_list":
            if BACK_ICON_REGION["x_start"] <= orig_x <= BACK_ICON_REGION["x_end"] and \
               BACK_ICON_REGION["y_start"] <= orig_y <= BACK_ICON_REGION["y_end"]:
                self.show_page("food_menu"); return
            if DELETE_MENU_BUTTON["x_start"] <= orig_x <= DELETE_MENU_BUTTON["x_end"] and \
               DELETE_MENU_BUTTON["y_start"] <= orig_y <= DELETE_MENU_BUTTON["y_end"]:
                self.prompt_for_deletion(); return
            if CONFIRM_BUTTON_REGION["x_start"] <= orig_x <= CONFIRM_BUTTON_REGION["x_end"] and \
               CONFIRM_BUTTON_REGION["y_start"] <= orig_y <= CONFIRM_BUTTON_REGION["y_end"]:
                if not any(qty > 0 for qty in self.cart.values()):
                    messagebox.showwarning("ตะกร้าว่างเปล่า", "กรุณาเพิ่มรายการอาหารก่อนยืนยัน")
                else:
                    order_summary = "\n".join([f"- {item} x {qty}" for item, qty in self.cart.items() if qty > 0])
                    if messagebox.askyesno("ยืนยันคำสั่งซื้อ", f"ส่งคำสั่งซื้อนี้?\n\n{order_summary}"):
                        if self.save_order_to_db():
                            messagebox.showinfo("ส่งสำเร็จ", "ส่งคำสั่งซื้อเรียบร้อยแล้ว!")
                            self.cart.clear(); self.show_page("food_menu")
                        else: messagebox.showerror("ผิดพลาด", "ไม่สามารถบันทึกคำสั่งซื้อได้")
                return
        
        elif page == "summary_page":
            if BACK_ICON_REGION["x_start"] <= orig_x <= BACK_ICON_REGION["x_end"] and \
               BACK_ICON_REGION["y_start"] <= orig_y <= BACK_ICON_REGION["y_end"]:
                self.show_page("table_page"); return 
            
            if SUMMARY_ADD_ITEM_REGION["x_start"] <= orig_x <= SUMMARY_ADD_ITEM_REGION["x_end"] and \
               SUMMARY_ADD_ITEM_REGION["y_start"] <= orig_y <= SUMMARY_ADD_ITEM_REGION["y_end"]:
                self.show_page("add_item_page"); return
                
            if SUMMARY_GOTO_ORDER_REGION["x_start"] <= orig_x <= SUMMARY_GOTO_ORDER_REGION["x_end"] and \
               SUMMARY_GOTO_ORDER_REGION["y_start"] <= orig_y <= SUMMARY_GOTO_ORDER_REGION["y_end"]:
                self.show_page("order_status_page"); return

            if SUMMARY_ADMIN_EDIT_REGION["x_start"] <= orig_x <= SUMMARY_ADMIN_EDIT_REGION["x_end"] and \
               SUMMARY_ADMIN_EDIT_REGION["y_start"] <= orig_y <= SUMMARY_ADMIN_EDIT_REGION["y_end"]:
                self.show_page("admin_edit_page"); return
                
            if SUMMARY_MONEY_PAGE_REGION["x_start"] <= orig_x <= SUMMARY_MONEY_PAGE_REGION["x_end"] and \
               SUMMARY_MONEY_PAGE_REGION["y_start"] <= orig_y <= SUMMARY_MONEY_PAGE_REGION["y_end"]:
                self.show_page("money_page"); return

        elif page == "register_page":
            if BACK_ICON_REGION["x_start"] <= orig_x <= BACK_ICON_REGION["x_end"] and \
               BACK_ICON_REGION["y_start"] <= orig_y <= BACK_ICON_REGION["y_end"]:
                self.show_page("login"); return
            if REGISTER_CONFIRM_BUTTON_REGION["x_start"] <= orig_x <= REGISTER_CONFIRM_BUTTON_REGION["x_end"] and \
               REGISTER_CONFIRM_BUTTON_REGION["y_start"] <= orig_y <= REGISTER_CONFIRM_BUTTON_REGION["y_end"]:
                self.process_registration(); return
                
            profile_box = ORIG_REG_PROFILE_BOX
            if profile_box["x"] <= orig_x <= (profile_box["x"] + profile_box["width"]) and \
               profile_box["y"] <= orig_y <= (profile_box["y"] + profile_box["height"]):
                self.select_profile_image(None) 
                return

        elif page == "forgot_page":
            if BACK_ICON_REGION["x_start"] <= orig_x <= BACK_ICON_REGION["x_end"] and \
               BACK_ICON_REGION["y_start"] <= orig_y <= BACK_ICON_REGION["y_end"]:
                self.show_page("login"); return
            if FORGOT_CONFIRM_BUTTON_REGION["x_start"] <= orig_x <= FORGOT_CONFIRM_BUTTON_REGION["x_end"] and \
               FORGOT_CONFIRM_BUTTON_REGION["y_start"] <= orig_y <= FORGOT_CONFIRM_BUTTON_REGION["y_end"]:
                self.process_forgot_password(); return

        elif page == "admin_edit_page":
            if BACK_ICON_REGION["x_start"] <= orig_x <= BACK_ICON_REGION["x_end"] and \
               BACK_ICON_REGION["y_start"] <= orig_y <= BACK_ICON_REGION["y_end"]:
                self.show_page("summary_page"); return 
            
            # 🟢 NEW: เพิ่มปุ่มกลับหน้ารวม (X: 472 , Y: 502)
            if ADMIN_BACK_TO_SUMMARY_REGION["x_start"] <= orig_x <= ADMIN_BACK_TO_SUMMARY_REGION["x_end"] and \
               ADMIN_BACK_TO_SUMMARY_REGION["y_start"] <= orig_y <= ADMIN_BACK_TO_SUMMARY_REGION["y_end"]:
                self.show_page("summary_page"); return

            # 🟢 NEW: เช็คปุ่ม "แก้ไข" (ปุ่มกลาง) (X: 681 , Y: 512)
            if ADMIN_EDIT_TABLE_BUTTON_REGION["x_start"] <= orig_x <= ADMIN_EDIT_TABLE_BUTTON_REGION["x_end"] and \
               ADMIN_EDIT_TABLE_BUTTON_REGION["y_start"] <= orig_y <= ADMIN_EDIT_TABLE_BUTTON_REGION["y_end"]:
                self.admin_prompt_for_table_edit(); return
            
            # 🟢 NEW: เช็คการคลิกบนโต๊ะ (เหมือนหน้า table_page)
            for i, region in enumerate(TABLE_REGIONS):
                if region["x_start"] <= orig_x <= region["x_end"] and region["y_start"] <= orig_y <= region["y_end"]:
                    table_number = i + 1
                    print(f"Admin clicked on Table {table_number}")
                    self.admin_manage_table_popup(table_number)
                    return

        elif page == "profile_page":
            if BACK_ICON_REGION["x_start"] <= orig_x <= BACK_ICON_REGION["x_end"] and \
               BACK_ICON_REGION["y_start"] <= orig_y <= BACK_ICON_REGION["y_end"]:
                self.show_page("login") 
                return
            
            if PROFILE_EDIT_BUTTON_REGION["x_start"] <= orig_x <= PROFILE_EDIT_BUTTON_REGION["x_end"] and \
               PROFILE_EDIT_BUTTON_REGION["y_start"] <= orig_y <= PROFILE_EDIT_BUTTON_REGION["y_end"]:
                self.toggle_profile_edit_mode(True); return
                
            if PROFILE_CONFIRM_BUTTON_REGION["x_start"] <= orig_x <= PROFILE_CONFIRM_BUTTON_REGION["x_end"] and \
               PROFILE_CONFIRM_BUTTON_REGION["y_start"] <= orig_y <= PROFILE_CONFIRM_BUTTON_REGION["y_end"]:
                self.save_profile_changes(); return
        
        elif page == "add_item_page":
            if BACK_ICON_REGION["x_start"] <= orig_x <= BACK_ICON_REGION["x_end"] and \
               BACK_ICON_REGION["y_start"] <= orig_y <= BACK_ICON_REGION["y_end"]:
                self.show_page("summary_page"); return
            
            if ADD_ITEM_CONFIRM_REGION["x_start"] <= orig_x <= ADD_ITEM_CONFIRM_REGION["x_end"] and \
               ADD_ITEM_CONFIRM_REGION["y_start"] <= orig_x <= ADD_ITEM_CONFIRM_REGION["y_end"]:
                self.process_add_item(); return
                
            # 🟢 NEW: ปุ่มยืนยันอันใหม่ (X: 1200 , Y: 638)
            if ADD_ITEM_CONFIRM_REGION_NEW["x_start"] <= orig_x <= ADD_ITEM_CONFIRM_REGION_NEW["x_end"] and \
               ADD_ITEM_CONFIRM_REGION_NEW["y_start"] <= orig_y <= ADD_ITEM_CONFIRM_REGION_NEW["y_end"]:
                self.process_add_item(); return
                
            if DELETE_ITEM_BUTTON_REGION["x_start"] <= orig_x <= DELETE_ITEM_BUTTON_REGION["x_end"] and \
               DELETE_ITEM_BUTTON_REGION["y_start"] <= orig_y <= DELETE_ITEM_BUTTON_REGION["y_end"]:
                self.prompt_delete_menu_item(); return

            img_box = ORIG_ADD_ITEM_IMAGE_BOX
            if img_box["x"] <= orig_x <= (img_box["x"] + img_box["width"]) and \
               img_box["y"] <= orig_y <= (img_box["y"] + img_box["height"]):
                self.select_add_item_image(None)
                return
                
        elif page == "order_status_page":
            if BACK_ICON_REGION["x_start"] <= orig_x <= BACK_ICON_REGION["x_end"] and \
               BACK_ICON_REGION["y_start"] <= orig_y <= BACK_ICON_REGION["y_end"]:
                self.show_page("summary_page"); return
        
        elif page == "money_page":
            if BACK_ICON_REGION["x_start"] <= orig_x <= BACK_ICON_REGION["x_end"] and \
               BACK_ICON_REGION["y_start"] <= orig_y <= BACK_ICON_REGION["y_end"]:
                self.show_page("summary_page"); return

            # 🟢 (แก้ไข) ตรวจสอบปุ่ม 1-6 คน
            if MONEY_BTN_1_REGION["x_start"] <= orig_x <= MONEY_BTN_1_REGION["x_end"] and \
               MONEY_BTN_1_REGION["y_start"] <= orig_y <= MONEY_BTN_1_REGION["y_end"]:
                print("Clicked 1 Person")
                self.process_payment(1); return
                
            if MONEY_BTN_2_REGION["x_start"] <= orig_x <= MONEY_BTN_2_REGION["x_end"] and \
               MONEY_BTN_2_REGION["y_start"] <= orig_y <= MONEY_BTN_2_REGION["y_end"]:
                print("Clicked 2 People")
                self.process_payment(2); return

            if MONEY_BTN_3_REGION["x_start"] <= orig_x <= MONEY_BTN_3_REGION["x_end"] and \
               MONEY_BTN_3_REGION["y_start"] <= orig_y <= MONEY_BTN_3_REGION["y_end"]:
                print("Clicked 3 People")
                self.process_payment(3); return
                
            if MONEY_BTN_4_REGION["x_start"] <= orig_x <= MONEY_BTN_4_REGION["x_end"] and \
               MONEY_BTN_4_REGION["y_start"] <= orig_y <= MONEY_BTN_4_REGION["y_end"]:
                print("Clicked 4 People")
                self.process_payment(4); return

            if MONEY_BTN_5_REGION["x_start"] <= orig_x <= MONEY_BTN_5_REGION["x_end"] and \
               MONEY_BTN_5_REGION["y_start"] <= orig_y <= MONEY_BTN_5_REGION["y_end"]:
                print("Clicked 5 People")
                self.process_payment(5); return

            if MONEY_BTN_6_REGION["x_start"] <= orig_x <= MONEY_BTN_6_REGION["x_end"] and \
               MONEY_BTN_6_REGION["y_start"] <= orig_y <= MONEY_BTN_6_REGION["y_end"]:
                print("Clicked 6 People")
                self.process_payment(6); return

            # 🟢 (แก้ไข) ตรวจสอบปุ่มกำหนดเอง
            if MONEY_BTN_CUSTOM_REGION["x_start"] <= orig_x <= MONEY_BTN_CUSTOM_REGION["x_end"] and \
               MONEY_BTN_CUSTOM_REGION["y_start"] <= orig_y <= MONEY_BTN_CUSTOM_REGION["y_end"]:
                print("Clicked Custom")
                self.process_payment_custom(); return
        
        # 🟢 NEW: (เพิ่ม)
        elif page == "bill_page":
            if BACK_ICON_REGION["x_start"] <= orig_x <= BACK_ICON_REGION["x_end"] and \
               BACK_ICON_REGION["y_start"] <= orig_y <= BACK_ICON_REGION["y_end"]:
                self.show_page("money_page"); return # (กลับไปหน้าเงิน)

        elif page == "fix_page": # 🟢 NEW
            if BACK_ICON_REGION["x_start"] <= orig_x <= BACK_ICON_REGION["x_end"] and \
               BACK_ICON_REGION["y_start"] <= orig_y <= BACK_ICON_REGION["y_end"]:
                self.show_page("login"); return
            
            # ----------------------------------------------------------------------
            # 🟢 START: (แก้ไข 3) เปลี่ยนพิกัดปุ่มยืนยันหน้าแก้
            # ----------------------------------------------------------------------
            if FIX_PAGE_CONFIRM_REGION["x_start"] <= orig_x <= FIX_PAGE_CONFIRM_REGION["x_end"] and \
               FIX_PAGE_CONFIRM_REGION["y_start"] <= orig_y <= FIX_PAGE_CONFIRM_REGION["y_end"]:
                print("Fix Page Confirm Clicked")
                self.validate_fix_page_login() # 🟢 (เพิ่ม) เรียกใช้ฟังก์ชันตรวจสอบใหม่
                return
            # ----------------------------------------------------------------------
            # 🟢 END: (แก้ไข 3)
            # ----------------------------------------------------------------------
            


    # --- หมวดที่ 13: เมธอดการกระทำและการตรวจสอบ (Action/Validation Methods) ---

    def admin_prompt_for_table_edit(self):
        """
        🟢 NEW: หน้าต่างถามหมายเลขโต๊ะที่จะแก้ไข (เรียกโดยปุ่ม "แก้ไข")
        """
        table_num = simpledialog.askinteger(
            "เลือกโต๊ะ", 
            f"กรุณากรอกหมายเลขโต๊ะที่ต้องการแก้ไข (1-{len(TABLE_CENTERS)}):",
            parent=self, minvalue=1, maxvalue=len(TABLE_CENTERS)
        )
        
        if table_num is not None:
            self.admin_manage_table_popup(table_num)

    def admin_manage_table_popup(self, table_number):
        """
        🟢 NEW HELPER: ฟังก์ชันสำหรับป๊อปอัพจัดการสถานะโต๊ะ (สำหรับหน้า Admin)
        """
        if table_number < 1 or table_number > len(self.table_status):
            messagebox.showerror("ผิดพลาด", "หมายเลขโต๊ะไม่ถูกต้อง")
            return
        
        table_index = table_number - 1
        current_status = self.table_status[table_index]
        status_text = "เต็ม (Occupied)" if current_status == 'occupied' else "ว่าง (Available)"

        action = messagebox.askyesnocancel(
            f"จัดการ โต๊ะ {table_number}",
            f"สถานะปัจจุบัน: {status_text}\n\n"
            " • กด 'Yes'  = ตั้งเป็น [เต็ม]\n"
            " • กด 'No'   = ตั้งเป็น [ว่าง]\n"
            " • กด 'Cancel' = ยกเลิก",
            parent=self
        )

        new_status = None
        if action is True:    # (Yes)
            new_status = 'occupied'
        elif action is False: # (No)
            new_status = 'available'

        if new_status and self.table_status[table_index] != new_status:
            self.table_status[table_index] = new_status
            print(f"✅ Admin set Table {table_number} status to: {new_status}")
            messagebox.showinfo("สำเร็จ", f"เปลี่ยนสถานะ โต๊ะ {table_number} เป็น {new_status} แล้ว")
            self.show_page("admin_edit_page")
        elif new_status:
            print(f"Table {table_number} status already '{new_status}'. No change.")
    
    def process_registration(self):
        username = self.reg_username_var.get().strip(); password = self.reg_password1_var.get().strip()
        confirm_password = self.reg_password2_var.get().strip(); phone = self.reg_phone_var.get().strip()
        email = self.reg_email_var.get().strip()
        if not all([username, password, confirm_password, phone, email]):
            messagebox.showwarning("ข้อมูลไม่ครบ", "กรุณากรอกข้อมูลให้ครบทุกช่อง"); return
        if not self.selected_profile_image_path:
            messagebox.showwarning("ต้องมีรูปโปรไฟล์", "กรุณาเลือกรูปโปรไฟล์"); return
        if password != confirm_password:
            messagebox.showerror("รหัสผ่านไม่ตรงกัน", "รหัสผ่านไม่ตรงกัน กรุณากรอกใหม่"); return
        if username.lower() == 'staff':
                 messagebox.showerror("ลงทะเบียนล้มเหลว", "ชื่อผู้ใช้ 'staff' ถูกสงวนไว้"); return
        if len(password) < 8:
            messagebox.showwarning("รหัสผ่านสั้นเกินไป", "รหัสผ่านต้องมีความยาวอย่างน้อย 8 ตัวอักษร")
            return
        if "@" not in email:
            messagebox.showwarning("รูปแบบอีเมลไม่ถูกต้อง", "กรุณากรอกอีเมลให้ถูกต้อง (ต้องมีเครื่องหมาย @)")
            return
        if not phone.isdigit():
            messagebox.showwarning("รูปแบบเบอร์โทรศัพท์ไม่ถูกต้อง", "เบอร์โทรศัพท์ต้องประกอบด้วยตัวเลขเท่านั้น")
            return
        if len(phone) != 10:
            messagebox.showwarning("รูปแบบเบอร์โทรศัพท์ไม่ถูกต้อง", "เบอร์โทรศัพท์ต้องมี 10 หลักพอดี")
            return
        saved_image_path_for_db = None
        try:
            _, file_extension = os.path.splitext(self.selected_profile_image_path)
            new_filename = f"{username}{file_extension}"
            destination_path = os.path.join(PROFILE_DIR, new_filename)
            shutil.copy(self.selected_profile_image_path, destination_path)
            saved_image_path_for_db = destination_path
            print(f"🖼️ Profile image saved to: {destination_path}")
        except Exception as e:
            print(f"🔴 ERROR copying profile image: {e}"); messagebox.showerror("ผิดพลาด", f"ไม่สามารถบันทึกรูปโปรไฟล์: {e}"); return
        conn = None
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if cursor.fetchone():
                messagebox.showerror("ชื่อผู้ใช้ซ้ำ", "ชื่อผู้ใช้นี้มีอยู่แล้ว กรุณาใช้ชื่ออื่น")
                if saved_image_path_for_db and os.path.exists(saved_image_path_for_db):
                    try: os.remove(saved_image_path_for_db); print("🧹 Cleaned up unused profile image.")
                    except OSError as oe: print(f"🔴 ERROR cleaning up image: {oe}")
                return
            cursor.execute("INSERT INTO users (username, password, phone, email, role, profile_image_path) VALUES (?, ?, ?, ?, ?, ?)",
                           (username, password, phone, email, 'user', saved_image_path_for_db))
            conn.commit()
            print(f"👤 New user '{username}' registered."); messagebox.showinfo("สมัครสำเร็จ", "สร้างบัญชีเรียบร้อย!\nกรุณากลับไปหน้าเข้าสู่ระบบ"); self.show_page("login")
        except sqlite3.Error as db_e:
            messagebox.showerror("Database Error", f"ไม่สามารถบันทึกข้อมูลผู้ใช้: {db_e}"); conn.rollback()
            if saved_image_path_for_db and os.path.exists(saved_image_path_for_db):
                try: os.remove(saved_image_path_for_db); print("🧹 Cleaned up profile image after DB error.")
                except OSError as oe: print(f"🔴 ERROR cleaning up image after DB error: {oe}")
        finally:
            if conn: conn.close()

    def process_forgot_password(self):
        email = self.forgot_email_var.get().strip(); phone = self.forgot_phone_var.get().strip()
        if not email or not phone: messagebox.showwarning("ข้อมูลไม่ครบ", "กรุณากรอก อีเมล และ เบอร์โทรศัพท์"); return
        conn = None
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE email = ? AND phone = ?", (email, phone))
            result = cursor.fetchone()
            if result: messagebox.showinfo("พบรหัสผ่าน", f"รหัสผ่านของคุณคือ: {result[0]}"); self.show_page("login")
            else: messagebox.showerror("ไม่พบข้อมูล", "ไม่พบผู้ใช้ที่ตรงกับ อีเมล และ เบอร์โทรศัพท์ ที่ระบุ")
        except sqlite3.Error as e: messagebox.showerror("Database Error", f"เกิดข้อผิดพลาดในการค้นหา: {e}")
        finally:
            if conn: conn.close()

    def prompt_for_deletion(self):
        sorted_cart_items = []
        for menu_item_spec in MENU_DATA:
            item_name = menu_item_spec["name"]
            if item_name in self.cart and self.cart[item_name] > 0:
                sorted_cart_items.append({"name": item_name, "qty": self.cart[item_name]})
        
        if not sorted_cart_items:
            messagebox.showwarning("ตะกร้าว่างเปล่า", "ไม่มีรายการให้ลบ"); return
        
        list_str = "รายการในตะกร้า:\n" + "\n".join([f"{i+1}. {item['name']} ({item['qty']} ชิ้น)" 
                                                     for i, item in enumerate(sorted_cart_items)])
        max_item_number = len(sorted_cart_items)
        
        item_number_to_delete = simpledialog.askinteger(
            "ลบรายการ (1/2)", f"{list_str}\n\nกรุณาป้อนหมายเลขรายการที่ต้องการลบ (1-{max_item_number}):",
            parent=self, minvalue=1, maxvalue=max_item_number
        )
        
        if item_number_to_delete is None: return
        
        try:
            selected_item_data = sorted_cart_items[item_number_to_delete - 1]
            item_name_to_delete = selected_item_data['name']
            current_qty = selected_item_data['qty']
        except IndexError:
            messagebox.showerror("ผิดพลาด", f"หมายเลขรายการไม่ถูกต้อง: {item_number_to_delete}"); return
        
        qty_to_delete = simpledialog.askinteger(
            "ลบรายการ (2/2)", f"รายการ: {item_number_to_delete}. {item_name_to_delete}\nจำนวนปัจจุบัน: {current_qty}\n\nกรอกจำนวนที่ต้องการลบ:",
            parent=self, minvalue=1, maxvalue=current_qty
        )
        
        if qty_to_delete is not None and messagebox.askyesno(
                "ยืนยันการลบ", f"ลบ '{item_name_to_delete}' จำนวน {qty_to_delete} ชิ้น?"):
            self.change_cart_quantity(item_name_to_delete, -qty_to_delete)
            messagebox.showinfo("ลบสำเร็จ", f"ลบ '{item_name_to_delete}' จำนวน {qty_to_delete} ชิ้นแล้ว")
            self.update_order_list_display()

    def validate_login(self, username, password):
        if not username or not password: messagebox.showerror("เข้าสู่ระบบล้มเหลว", "กรุณากรอก ชื่อผู้ใช้ และ รหัสผ่าน"); return
        conn = None
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute("SELECT password, role, profile_image_path FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()
            if result and password == result[0]:
                _, user_role, stored_image_path = result
                messagebox.showinfo("เข้าสู่ระบบสำเร็จ", f"ยินดีต้อนรับ, {username}!")
                self.current_user_profile_path = stored_image_path
                self.username_var.set(username) 
                print(f"👤 User '{username}' logged in. Role: {user_role}. Profile path: {stored_image_path}")
                
                # 🟢 (แก้ไข) ถ้าเป็น Staff ให้ไปหน้า 'summary_page' (หน้ารวม) เลย
                if user_role == 'staff':
                    self.show_page("summary_page")
                else:
                    if self.selected_table_index is not None:
                        table_num = self.selected_table_index + 1
                        print(f"🟢 Table {table_num} is now occupied.")
                        self.table_status[self.selected_table_index] = 'occupied'
            
                    self.show_page("food_menu")
                
            else: messagebox.showerror("เข้าสู่ระบบล้มเหลว", "ชื่อผู้ใช้ หรือ รหัสผ่าน ไม่ถูกต้อง")
        except sqlite3.Error as e: messagebox.showerror("Database Error", f"เกิดข้อผิดพลาด: {e}")
        finally:
            if conn: conn.close()

    def validate_admin_lookup(self):
        username = self.admin_username_var.get().strip()
        password = self.admin_password_var.get().strip()
        if not username or not password:
            messagebox.showwarning("ข้อมูลไม่ครบ", "กรุณากรอก Username และ Password ที่ต้องการค้นหา")
            return

        conn = None
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT username, phone, email, profile_image_path, password, role FROM users WHERE username = ? AND password = ?", (username, password))
            result = cursor.fetchone()

            if result:
                self.lookup_user_data = dict(result)
                print(f"🧑‍💻 Found user data for '{username}'. Navigating to profile page.")
                self.show_page("profile_page")
            else:
                messagebox.showerror("ไม่พบผู้ใช้", "ไม่พบ Username หรือ Password นี้ในระบบ")
                self.lookup_user_data = {}

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"เกิดข้อผิดพลาดในการค้นหา: {e}")
            self.lookup_user_data = {}
        finally:
            if conn: conn.close()

    # ----------------------------------------------------------------------
    # 🟢 START: (เพิ่ม) ฟังก์ชันตรวจสอบสำหรับหน้า Fix Page
    # ----------------------------------------------------------------------
    def validate_fix_page_login(self):
        """ 🟢 NEW: Validates login from 'fix_page' to go to 'profile_page'. """
        username = self.fix_username_var.get().strip()
        password = self.fix_password_var.get().strip()
        if not username or not password:
            messagebox.showwarning("ข้อมูลไม่ครบ", "กรุณากรอก Username และ Password", parent=self)
            return

        conn = None
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            conn.row_factory = sqlite3.Row # ⭐️ สำคัญ: เพื่อให้ lookup_user_data (dict) ทำงาน
            cursor = conn.cursor()
            
            # ⭐️ ใช้ SQL query เดียวกับ validate_admin_lookup
            cursor.execute("SELECT username, phone, email, profile_image_path, password, role FROM users WHERE username = ? AND password = ?", (username, password))
            result = cursor.fetchone()

            if result:
                self.lookup_user_data = dict(result)
                print(f"🧑‍💻 [Fix Page] Found user data for '{username}'. Navigating to profile page.")
                self.show_page("profile_page")
            else:
                messagebox.showerror("ไม่พบผู้ใช้", "ไม่พบ Username หรือ Password นี้ในระบบ", parent=self)
                self.lookup_user_data = {}

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"เกิดข้อผิดพลาดในการค้นหา: {e}", parent=self)
            self.lookup_user_data = {}
        finally:
            if conn: conn.close()
    # ----------------------------------------------------------------------
    # 🟢 END: (เพิ่ม)
    # ----------------------------------------------------------------------
        
    def lookup_user_data_by_username(self, username):
        """Looks up user data when a user clicks their own profile (no password check)."""
        if not username:
            print("🔴 Cannot lookup profile, username is blank.")
            return

        conn = None
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            
            cursor.execute("SELECT username, phone, email, profile_image_path, password, role FROM users WHERE username = ?", (username,))
            result = cursor.fetchone()

            if result:
                self.lookup_user_data = dict(result)
                print(f"🧑‍💻 Found self-profile data for '{username}'.")
            else:
                print(f"🔴 Could not find self-profile data for '{username}'.")
                self.lookup_user_data = {}

        except sqlite3.Error as e:
            print(f"🔴 DB Error looking up self-profile: {e}")
            self.lookup_user_data = {}
        finally:
            if conn: conn.close()

    def toggle_profile_edit_mode(self, edit_mode):
        """Toggles the entry fields on the profile page between readonly and normal."""
        new_state = "normal" if edit_mode else "readonly"
        bg_color = "#FFFFFF" if edit_mode else "#F0F0F0" 
        
        if hasattr(self, 'profile_phone_display'):
            self.profile_phone_display.config(state=new_state, readonlybackground=bg_color, bg=bg_color)
        if hasattr(self, 'profile_email_display'):
            self.profile_email_display.config(state=new_state, readonlybackground=bg_color, bg=bg_color)
        if hasattr(self, 'profile_password_display'):
            self.profile_password_display.config(state=new_state, readonlybackground=bg_color, bg=bg_color)
            
        if hasattr(self, 'profile_username_display'):
            self.profile_username_display.config(state='readonly', readonlybackground="#F0F0F0", bg="#F0F0F0")

        self.profile_edit_mode.set(edit_mode)
        print(f"Profile edit mode set to: {edit_mode}")

    def save_profile_changes(self):
        """Saves the edited profile data to the database."""
        if not self.profile_edit_mode.get():
            messagebox.showinfo("ไม่มีการเปลี่ยนแปลง", "กด 'แก้ไข' ก่อนจึงจะยืนยันได้")
            return

        username = self.profile_display_username.get()
        if not username or username == "N/A":
            messagebox.showerror("ผิดพลาด", "ไม่พบชื่อผู้ใช้ (Username) ที่จะอัปเดต")
            return

        new_phone = self.profile_display_phone.get().strip()
        new_email = self.profile_display_email.get().strip()
        new_password = self.profile_display_password.get().strip()

        if not all([new_phone, new_email, new_password]):
            messagebox.showwarning("ข้อมูลไม่ครบ", "กรุณากรอกข้อมูลให้ครบทุกช่อง (Phone, Email, Password)"); return
        if len(new_password) < 8:
            messagebox.showwarning("รหัสผ่านสั้นเกินไป", "รหัสผ่านต้องมีความยาวอย่างน้อย 8 ตัวอักษร"); return
        if "@" not in new_email:
            messagebox.showwarning("รูปแบบอีเมลไม่ถูกต้อง", "กรุณากรอกอีเมลให้ถูกต้อง"); return
        if not new_phone.isdigit() or len(new_phone) != 10:
            messagebox.showwarning("รูปแบบเบอร์โทรศัพท์ไม่ถูกต้อง", "เบอร์โทรศัพท์ต้องมี 10 หลัก (ตัวเลขเท่านั้น)"); return

        if not messagebox.askyesno("ยืนยันการแก้ไข", f"คุณต้องการอัปเดตข้อมูลสำหรับ '{username}' ใช่หรือไม่?"):
            return
            
        conn = None
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE users 
                SET phone = ?, email = ?, password = ?
                WHERE username = ?
            """, (new_phone, new_email, new_password, username))
            conn.commit()
            
            if cursor.rowcount > 0:
                messagebox.showinfo("สำเร็จ", f"อัปเดตข้อมูลสำหรับ '{username}' เรียบร้อยแล้ว")
                self.lookup_user_data['phone'] = new_phone
                self.lookup_user_data['email'] = new_email
                self.lookup_user_data['password'] = new_password
                self.toggle_profile_edit_mode(False) 
            else:
                messagebox.showerror("ผิดพลาด", f"ไม่สามารถอัปเดตข้อมูลสำหรับ '{username}' (ไม่พบใน DB)")

        except sqlite3.Error as e:
            messagebox.showerror("Database Error", f"เกิดข้อผิดพลาด: {e}")
            if conn: conn.rollback()
        finally:
            if conn: conn.close()

    def save_order_to_db(self):
        items_to_insert = [(item, qty) for item, qty in self.cart.items() if qty > 0]
        if not items_to_insert: 
            print("🛒 Cart is empty."); 
            return False
            
        table_name = self.current_table_name_var.get()
        if not table_name:
            print("🔴 ERROR: Cannot save order, no table name selected.")
            messagebox.showerror("ผิดพลาด", "ไม่พบชื่อโต๊ะ")
            return False
            
        conn = None
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            
            cursor.execute("INSERT INTO Orders (table_name, status) VALUES (?, ?)", (table_name, 'pending'))
            new_order_id = cursor.lastrowid
            
            db_data = [(new_order_id, item, qty) for item, qty in items_to_insert]
            cursor.executemany("INSERT INTO Menu (order_id, item_name, quantity) VALUES (?, ?, ?)", db_data)
            
            conn.commit()
            print(f"✅ Order {new_order_id} saved for {table_name} ({len(db_data)} items)."); 
            return True
        except sqlite3.Error as e:
            print(f"🔴 ERROR saving order: {e}"); 
            conn.rollback(); 
            return False
        finally:
            if conn: conn.close()
            
    # ----------------------------------------------------------------------
    # 🟢 START: (แก้ไข) ลบ "ราคา" + แก้ไขการแทรกเมนู
    # ----------------------------------------------------------------------
    def process_add_item(self):
        global MENU_DATA, FOOD_ITEMS_LIST 
        
        item_name = self.add_item_name_var.get().strip()
        category = self.add_item_category_var.get().strip()
        image_path = self.add_item_image_path
        
        # --- Validation ---
        if not item_name or not image_path:
            messagebox.showwarning("ข้อมูลไม่ครบ", "กรุณากรอก ชื่อ และเลือกรูปภาพ")
            return
        
        if category == CATEGORY_OPTIONS[0]: 
            messagebox.showwarning("ข้อมูลไม่ครบ", "กรุณาเลือกประเภทของสินค้า")
            return
            
        price = 0 # 🟢 NEW: ตั้งราคาเป็น 0
        
        # --- Process Image ---
        try:
            _, file_extension = os.path.splitext(image_path)
            new_filename = f"{item_name}{file_extension}"
            
            destination_path = os.path.join(BASE_DIR, new_filename)
            
            shutil.copy(image_path, destination_path)
            print(f"🖼️ New item image saved to: {destination_path}")

        except Exception as e:
            print(f"🔴 ERROR copying item image: {e}"); 
            messagebox.showerror("ผิดพลาด", f"ไม่สามารถบันทึกรูปสินค้า: {e}"); 
            return

        # --- Process Data ---
        new_item_dict = {
            "category": category,
            "name": item_name,
            "image": new_filename,
            "description": "", 
            "price": price # 🟢 CHANGED: ใช้ราคา 0
        }
        
        # 🟢 (แก้ไข) ตรรกะการแทรกเมนู
        inserted = False
        for i, item in enumerate(MENU_DATA):
            if item["category"] == category:
                # หา item สุดท้ายของหมวดหมู่นี้
                for j in range(i, len(MENU_DATA)):
                    if MENU_DATA[j]["category"] != category:
                        # แทรกก่อนที่หมวดหมู่ใหม่จะเริ่ม
                        MENU_DATA.insert(j, new_item_dict)
                        inserted = True
                        break
                if not inserted:
                    # ถ้าเจอหมวดหมู่ แต่หาจุดสิ้นสุดไม่เจอ (แสดงว่าเป็นหมวดหมู่สุดท้าย)
                    MENU_DATA.append(new_item_dict)
                    inserted = True
                break
        
        if not inserted:
            # ถ้าไม่เจอหมวดหมู่นี้เลย (เป็นหมวดหมู่ใหม่)
            MENU_DATA.append(new_item_dict)
        
        FOOD_ITEMS_LIST = [item['name'] for item in MENU_DATA]
        
        messagebox.showinfo("สำเร็จ", f"เพิ่มสินค้า '{item_name}' ลงในเมนูเรียบร้อยแล้ว")
        
        if hasattr(self, 'menu_items_frame') and self.menu_items_frame:
            self._load_menu_items()
            
        self.show_page("summary_page") 
    # ----------------------------------------------------------------------
    # 🟢 END: (แก้ไข)
    # ----------------------------------------------------------------------

    def prompt_delete_menu_item(self):
        """Prompts the admin to delete an item from the global MENU_DATA."""
        global MENU_DATA, FOOD_ITEMS_LIST 

        item_names = [item['name'] for item in MENU_DATA]
        if not item_names:
            messagebox.showinfo("เมนูว่าง", "ไม่มีรายการอาหารให้ลบ")
            return
        
        list_str = "รายการอาหารทั้งหมด:\n" + "\n".join([f"{i+1}. {name}" for i, name in enumerate(item_names)])
        max_num = len(item_names)
        
        num_to_delete = simpledialog.askinteger("ลบรายการ (1/2)", 
            f"{list_str}\n\nป้อนหมายเลขที่ต้องการลบ (1-{max_num}):", 
            parent=self, minvalue=1, maxvalue=max_num)
        
        if num_to_delete is None: return

        try:
            item_name_to_delete = item_names[num_to_delete - 1]
        except IndexError:
            messagebox.showerror("ผิดพลาด", "หมายเลขไม่ถูกต้อง")
            return 

        if messagebox.askyesno("ยืนยันการลบ", f"คุณต้องการลบ '{item_name_to_delete}' ออกจากเมนูหลักถาวรหรือไม่?\n(การเปลี่ยนแปลงนี้จะมีผลเมื่อคุณไปที่หน้าเมนู)"):
            
            original_len = len(MENU_DATA)
            MENU_DATA = [item for item in MENU_DATA if item['name'] != item_name_to_delete]
            
            if len(MENU_DATA) < original_len:
                messagebox.showinfo("ลบสำเร็จ", f"'{item_name_to_delete}' ถูกลบแล้ว")
                FOOD_ITEMS_LIST = [item['name'] for item in MENU_DATA]
                
                if hasattr(self, 'menu_items_frame') and self.menu_items_frame:
                    self._load_menu_items()
                    print("Menu frame refreshed after deletion.")
            else:
                messagebox.showerror("ผิดพลาด", "ไม่พบรายการที่จะลบ")

    def add_item_to_cart(self, item_name, quantity):
        if quantity <= 0: return
        new_quantity = self.cart.get(item_name, 0) + quantity
        self.cart[item_name] = new_quantity
        print(f"🛒 Cart: Added '{item_name}' x {quantity}. Total: {self.cart.get(item_name, 0)}")

    def prompt_for_quantity(self, item_name):
        current_qty = self.cart.get(item_name, 0)
        quantity_to_add = simpledialog.askinteger(
            "เพิ่มจำนวนสินค้า",
            f"ต้องการเพิ่ม '{item_name}' กี่ชิ้น?\n(ปัจจุบันมีในตะกร้า: {current_qty} ชิ้น)",
            parent=self, minvalue=1, initialvalue=1
        )
        if quantity_to_add is not None:
            self.add_item_to_cart(item_name, quantity_to_add)

    def change_cart_quantity(self, item_name, delta):
        if delta >= 0:
            print("⚠️ change_cart_quantity ควรใช้สำหรับลดจำนวนเท่านั้น. ใช้ add_item_to_cart สำหรับเพิ่ม.")
            return

        new_quantity = self.cart.get(item_name, 0) + delta
        if new_quantity > 0: self.cart[item_name] = new_quantity
        elif new_quantity == 0:
            if item_name in self.cart:
                del self.cart[item_name]; print(f"➖ Removed '{item_name}'.")
        else: print(f"⚠️ Cannot reduce '{item_name}' below zero."); return
        print(f"🛒 Cart: '{item_name}' = {self.cart.get(item_name, 0)}")
        if self.current_page == "order_list": self.update_order_list_display()

    def process_payment(self, person_count):
        """ 🟢 NEW: คำนวณราคาและแสดง QR popup """
        if person_count <= 0: return
        # 🟢 (ใช้ค่าคงที่)
        total_price = person_count * MONEY_PRICE_PER_PERSON 
        print(f"Processing payment for {person_count} people. Total: {total_price} THB")
        
        # 🟢 (แก้ไข) เก็บค่าไว้สำหรับหน้าบิล
        self.final_bill_amount = total_price
        self.final_bill_person_count = person_count
        
        # 🟢 (เรียก Pop-up)
        self._show_payment_popup(f"สำหรับ {person_count} คน", total_price) 

    def process_payment_custom(self):
        """ 🟢 NEW: ถามจำนวนคนแบบกำหนดเอง """
        person_count = simpledialog.askinteger(
            "กรอกจำนวนคน", 
            "กรุณากรอกจำนวนคนที่ต้องการชำระเงิน:",
            parent=self, minvalue=1
        )
        if person_count is not None and person_count > 0:
            self.process_payment(person_count)
        else:
            print("Custom payment cancelled.")
            
    # 🟢 (เพิ่ม) ฟังก์ชันตัวช่วยสำหรับปุ่มยืนยัน
    def _on_confirm_payment(self, popup_window):
        """ 🟢 NEW: (เพิ่ม) ถูกเรียกเมื่อกดยืนยันใน QR Popup """
        print("Payment confirmed. Closing popup and going to Bill Page.")
        popup_window.destroy()
        self.show_page("bill_page")

    # ----------------------------------------------------------------------
    # 🟢 START: (แก้ไข 1) ฟังก์ชัน Pop-up จ่ายเงิน
    # ----------------------------------------------------------------------
    def _show_payment_popup(self, person_name, amount):
        """
        🟢 NEW: สร้างหน้าต่าง Pop-up สำหรับแสดง QR Code จ่ายเงิน
        """
        popup = tk.Toplevel(self)
        popup.title(f"ชำระเงินสำหรับ {person_name}")
        popup.geometry("350x450") # ขนาดหน้าต่าง
        popup.configure(bg="#F0F8FF") # สีพื้นหลัง
        popup.resizable(False, False)
        
        # ----------------------------------------------------------------------
        # 🟢 START: (แก้ไข 1) เปลี่ยนชื่อไฟล์เป็น .jpg (ตามคำขอ)
        # ----------------------------------------------------------------------
        qr_image_path = os.path.join(BASE_DIR, "qr.jpg") # 🟢 NEW: (แก้ไข 1) เปลี่ยนเป็น qr.jpg
        # ----------------------------------------------------------------------
        # 🟢 END: (แก้ไข 1)
        # ----------------------------------------------------------------------
        
        try:
            qr_image_open = Image.open(qr_image_path)
            qr_image_resized = qr_image_open.resize((250, 250), Image.Resampling.LANCZOS)
            # ⭐️ ต้องเก็บ reference ของ PhotoImage ไว้
            self.qr_photo_tk = ImageTk.PhotoImage(qr_image_resized) 
            
            qr_label = tk.Label(popup, image=self.qr_photo_tk, bg="#F0F8FF")
            qr_label.pack(pady=20)

        except FileNotFoundError:
            # 🟢 (แก้ไข 1) อัปเดตข้อความ Error ให้ตรง
            print(f"🔴 ERROR: ไม่พบไฟล์ 'qr.jpg' ที่: {qr_image_path}") # 🟢 NEW: (แก้ไข 1) อัปเดตข้อความ Error
            qr_label = tk.Label(popup, 
                                text="ไม่พบไฟล์ 'qr.jpg'!", # 🟢 NEW: (แก้ไข 1) อัปเดตข้อความ Error
                                fg="red", bg="#F0F8FF", font=("Arial", 16, "bold"))
            qr_label.pack(pady=(100, 20)) # จัดให้อยู่กลางๆ
        except Exception as e:
            # 🟢 (แก้ไข 1) อัปเดตข้อความ Error (กรณีไฟล์ .pdf จริง)
            print(f"🔴 ERROR loading {qr_image_path}: {e}")
            error_text = f"เกิดข้อผิดพลาด: {e}\n\n(ไม่สามารถโหลด 'qr.jpg')" # 🟢 NEW: (แก้ไข 1) อัปเดตข้อความ Error
            qr_label = tk.Label(popup, text=error_text, fg="red", bg="#F0F8FF", font=("Arial", 12))
            qr_label.pack(pady=(100, 20))

        # --- แสดงจำนวนเงิน ---
        amount_label = tk.Label(popup, 
                                text=f"จำนวนเงิน: {amount} บาท", 
                                font=("Arial", 18, "bold"), 
                                bg="#F0F8FF")
        amount_label.pack(pady=10)

        # --- ปุ่มยืนยัน ---
        confirm_button = tk.Button(popup, 
                                   text="ยืนยัน", 
                                   font=("Arial", 14), 
                                   width=15,
                                   bg="#4CAF50", fg="white", 
                                   # 🟢 (แก้ไข) เปลี่ยนคำสั่ง
                                   command=lambda: self._on_confirm_payment(popup))
        confirm_button.pack(pady=15)
        
        # --- ทำให้หน้าต่างนี้อยู่บนสุด ---
        popup.grab_set() # บังคับให้ focus
        popup.wait_window() # รอจนกว่าหน้าต่างนี้จะปิด
    # ----------------------------------------------------------------------
    # 🟢 END: (แก้ไข 1)
    # ----------------------------------------------------------------------


# --- หมวดที่ 14: ฟังก์ชันช่วยโหลดรูปภาพ (Image Loading Helpers) ---

    def select_profile_image(self, event):
        filepath = filedialog.askopenfilename(title="เลือกรูปโปรไฟล์", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All Files", "*.*")])
        if filepath: 
            self.selected_profile_image_path = filepath
            self._on_resize_register_page(None)

    def select_add_item_image(self, event):
        filepath = filedialog.askopenfilename(title="เลือกรูปสินค้า", filetypes=[("Image Files", "*.png *.jpg *.jpeg *.gif *.bmp"), ("All Files", "*.*")])
        if filepath:
            self.add_item_image_path = filepath
            self._on_resize_add_item_page(None)

    def _load_image_to_label(self, path, target_label, target_tk_attr_name, size):
        w, h = size
        if w <= 0 or h <= 0 or not path or not os.path.exists(path):
            if hasattr(self, target_label): getattr(self, target_label).config(image=None, text="No Pic")
            print(f"🟠 WARNING: Image not found or invalid size for {target_label}: '{path}'")
            return False
        try:
            image = Image.open(path)
            if getattr(image, "is_animated", False): image.seek(0)
            image.thumbnail(size, Image.Resampling.LANCZOS)
            photo_image = ImageTk.PhotoImage(image)
            setattr(self, target_tk_attr_name, photo_image)
            if hasattr(self, target_label): getattr(self, target_label).config(image=photo_image, text="")
            return True
        except Exception as e:
            print(f"🔴 ERROR loading image '{path}' for {target_label}: {e}")
            if hasattr(self, target_label): getattr(self, target_label).config(image=None, text="Load Err")
            return False

    def load_register_profile_preview(self, path, size):
        self._load_image_to_label(path, 'reg_profile_label', 'reg_profile_preview_tk', size)

    def load_menu_profile_image_resized(self, path, size):
        self._load_image_to_label(path, 'menu_profile_label', 'menu_profile_image_tk', size)

    def load_profile_page_image_resized(self, path, size):
        self._load_image_to_label(path, 'profile_image_label', 'profile_page_image_tk', size)
        
    def load_add_item_image_preview(self, path, size):
        self._load_image_to_label(path, 'add_item_image_label', 'add_item_image_preview_tk', size)

    def load_placeholder_image(self, target_label, target_tk_attr, size):
        if not self.original_placeholder_image:
            print("🔴 ERROR: ไม่ได้โหลด original_placeholder_image")
            return
            
        w, h = size
        if w <= 0 or h <= 0: return

        try:
            image = self.original_placeholder_image.copy()
            image.thumbnail(size, Image.Resampling.LANCZOS)
            photo_image = ImageTk.PhotoImage(image)
            setattr(self, target_tk_attr, photo_image)
            if hasattr(self, target_label):
                getattr(self, target_label).config(image=photo_image, text="")
        except Exception as e:
            print(f"🔴 ERROR loading placeholder image: {e}")


# --- หมวดที่ 15: ฟังก์ชันช่วยเลื่อน (Scrolling Helper) ---
    
    def scroll_menu_to_y(self, target_y):
        if self.current_page != "food_menu" or not hasattr(self, 'sub_canvas'): return
        try:
            orig_menu_height = 3802 
            fraction = min(1.0, max(0.0, float(target_y) / float(orig_menu_height)))
            
            self.sub_canvas.yview_moveto(fraction)
            print(f"📜 Scrolling menu sub-frame to Y={target_y} (frac={fraction:.4f})")
            
        except Exception as e: print(f"🔴 ERROR in scroll_menu_to_y: {e}")
    
    def scroll_to_y(self, target_y):
        if self.current_page != "food_menu" or not hasattr(self, 'main_canvas') or self.original_food_menu_image is None: return
        try:
            _, orig_height = self.original_food_menu_image.size
            if orig_height == 0: return
            scroll_pos_y = max(0, target_y - 50)
            fraction = min(1.0, max(0.0, float(scroll_pos_y) / float(orig_height)))
            self.main_canvas.yview_moveto(fraction)
            print(f"📜 Scrolling food menu background to Y={target_y} (frac={fraction:.4f})")
        except Exception as e: print(f"🔴 ERROR in scroll_to_y: {e}")


# --- หมวดที่ 16: เมธอดแสดงหน้า (Page Display Methods) ---

    def _create_canvas_with_scrollbar(self, parent_frame):
        canvas = tk.Canvas(parent_frame, highlightthickness=0, bg="#FFFFFF")
        v_scrollbar = tk.Scrollbar(parent_frame, orient="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=v_scrollbar.set)
        v_scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        return canvas

    def _setup_scrollable_frame(self, canvas, frame_bg="#F0F0F0"):
        scrollable_frame = tk.Frame(canvas, bg=frame_bg)
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", tags="frame")
        scrollable_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        
        scrollable_frame.bind('<Enter>', lambda e: self._bind_mousewheel(canvas))
        scrollable_frame.bind('<Leave>', lambda e: self._unbind_mousewheel(canvas))
        
        return scrollable_frame

    def _bind_mousewheel(self, canvas):
        canvas.bind_all("<MouseWheel>", lambda e: self._on_mousewheel(e, canvas))

    def _unbind_mousewheel(self, canvas):
        canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event, canvas):
        if event.num == 5 or event.delta == -120:
            canvas.yview_scroll(1, "units")
        if event.num == 4 or event.delta == 120:
            canvas.yview_scroll(-1, "units")

    def _place_and_scale_widget(self, widget, config, scale_factor, parent_widget, is_label=False, font_base_size=10, bold=False):
        if not config: return 0, 0
        x = int(config.get("x", 0) * scale_factor)
        y = int(config.get("y", 0) * scale_factor)
        w = int(config.get("width", 10) * scale_factor)
        h = int(config.get("height", 10) * scale_factor)

        font_scale = 0.4
        calculated_size = int(h * font_scale)
        font_size = max(6, calculated_size)

        font_style = "bold" if bold or is_label else "normal"
        widget.config(font=("Arial", font_size, font_style))
        widget.place(in_=parent_widget, x=x, y=y, width=w, height=h)
        return w, h


    # --- หน้าจอเลือกโต๊ะ (Table Selection) ---
    def show_table_page(self):
        self.main_canvas = self._create_canvas_with_scrollbar(self.content_frame)
        frame_bg = "#D9534F"
        self.scrollable_frame_table = self._setup_scrollable_frame(self.main_canvas, frame_bg)
        self.background_label = tk.Label(self.scrollable_frame_table, image=None, borderwidth=0, bg=frame_bg)
        self.background_label.pack()
        self.background_label.bind('<Button-1>', self.get_click_position)
        self.table_status_labels_table_page = [tk.Label(self.background_label, text="", font=("Arial", 10, "bold"), bg=frame_bg) for _ in TABLE_CENTERS]
        self.main_canvas.bind('<Configure>', self._on_resize_table_page)
        self.after(100, lambda: self._on_resize_table_page(None))

    def _on_resize_table_page(self, event):
        bg_image, tk_image_attr = self.original_table_page_image, 'table_bg_image_tk'
        if not bg_image: return
        canvas_width = self.main_canvas.winfo_width()
        if canvas_width < 50: return
        try:
            orig_width, orig_height = bg_image.size
            if orig_width == 0: return
            scale_factor = canvas_width / float(orig_width); self.current_scale_factor = scale_factor
            target_width, target_height = canvas_width, int(orig_height * scale_factor)
            resized_img = bg_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            setattr(self, tk_image_attr, ImageTk.PhotoImage(resized_img))
            self.background_label.config(image=getattr(self, tk_image_attr), width=target_width, height=target_height)
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

            for i, label in enumerate(self.table_status_labels_table_page):
                if i < len(TABLE_REGIONS) and i < len(TABLE_ALIGNMENT_CENTERS):
                    align_coords = TABLE_ALIGNMENT_CENTERS[i]
                    font_size = max(6, int(TABLE_CLICK_HEIGHT * scale_factor * 0.3))
                    label.config(font=("Arial", font_size, "bold"), bg='white')
                    orig_corner_x = align_coords["x"] + table_half_w; orig_corner_y = align_coords["y"] - table_half_h
                    corner_x = int(orig_corner_x * scale_factor); corner_y = int(orig_corner_y * scale_factor)
                    if self.table_status[i] == 'occupied': label.config(text="\u2717", fg="#E74C3C")
                    else: label.config(text="\u2713", fg="#2ECC71")
                    label.place(x=corner_x, y=corner_y, anchor="c")
                else: label.place_forget()
        except Exception as e: print(f"🔴 ERROR in _on_resize_table_page: {e}")

    # --- หน้าจอเข้าสู่ระบบ (Login) ---
    def show_login_page(self):
        self.main_canvas = self._create_canvas_with_scrollbar(self.content_frame)
        frame_bg = "#F7E6D5"
        self.scrollable_frame_login = self._setup_scrollable_frame(self.main_canvas, frame_bg)
        self.background_label = tk.Label(self.scrollable_frame_login, image=None, borderwidth=0, bg=frame_bg)
        self.background_label.pack(); self.background_label.bind('<Button-1>', self.get_click_position)
        self.login_username_text_label = tk.Label(self.background_label, text="ชื่อผู้ใช้:", font=("Arial", 10, "bold"), anchor="w", bg=frame_bg, fg="#C74136")
        self.login_password_text_label = tk.Label(self.background_label, text="รหัสผ่าน:", font=("Arial", 10, "bold"), anchor="w", bg=frame_bg, fg="#C74136")
        self.login_username_entry = tk.Entry(self.background_label, textvariable=self.username_var, font=("Arial", 12), relief="flat", bd=0, bg="white")
        self.login_password_entry = tk.Entry(self.background_label, textvariable=self.password_var, font=("Arial", 12), show="*", relief="flat", bd=0, bg="white")
        self.main_canvas.bind('<Configure>', self._on_resize_login)
        self.after(100, lambda: self._on_resize_login(None))

    def _on_resize_login(self, event):
        bg_image, tk_image_attr = self.original_login_image, 'login_bg_image_tk'
        if not bg_image: return
        canvas_width = self.main_canvas.winfo_width()
        if canvas_width < 50: return
        try:
            orig_width, orig_height = bg_image.size
            if orig_width == 0: return
            scale_factor = canvas_width / float(orig_width); self.current_scale_factor = scale_factor
            target_width, target_height = canvas_width, int(orig_height * scale_factor)
            resized_img = bg_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            setattr(self, tk_image_attr, ImageTk.PhotoImage(resized_img))
            self.background_label.config(image=getattr(self, tk_image_attr), width=target_width, height=target_height)
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
            self._place_and_scale_widget(self.login_username_text_label, ORIG_LOGIN_USERNAME_LABEL, scale_factor, self.background_label, is_label=True, bold=True)
            self._place_and_scale_widget(self.login_username_entry, ORIG_LOGIN_USERNAME_BOX, scale_factor, self.background_label)
            self._place_and_scale_widget(self.login_password_text_label, ORIG_LOGIN_PASSWORD_LABEL, scale_factor, self.background_label, is_label=True, bold=True)
            self._place_and_scale_widget(self.login_password_entry, ORIG_LOGIN_PASSWORD_BOX, scale_factor, self.background_label)
        except Exception as e: print(f"🔴 ERROR in _on_resize_login: {e}")

    # --- หน้าจอเมนูอาหาร (Food Menu) ---
    def show_food_menu(self):
        self.main_canvas = self._create_canvas_with_scrollbar(self.content_frame)
        self.scrollable_frame_food = self._setup_scrollable_frame(self.main_canvas, "#FFFFFF")
        
        self.background_label = tk.Label(self.scrollable_frame_food, image=None, borderwidth=0, bg="white")
        self.background_label.pack()
        self.background_label.bind('<Button-1>', self.get_click_position)
        
        self.sub_canvas = tk.Canvas(self.background_label, highlightthickness=0, bg="#FEFEFE", relief="flat", bd=0)
        
        self.sub_canvas_scrollbar = tk.Scrollbar(self.background_label, orient="vertical", command=self.sub_canvas.yview)
        self.sub_canvas.configure(yscrollcommand=self.sub_canvas_scrollbar.set)
        
        self.menu_items_frame = tk.Frame(self.sub_canvas, bg="#FEFEFE")
        self.sub_canvas.create_window((0, 0), window=self.menu_items_frame, anchor="nw", tags="menu_frame")
        self.menu_items_frame.bind("<Configure>", lambda e: self.sub_canvas.config(scrollregion=self.sub_canvas.bbox("all")))
        
        self.sub_canvas.bind('<Enter>', lambda e: self._bind_mousewheel(self.sub_canvas))
        self.sub_canvas.bind('<Leave>', lambda e: self._unbind_mousewheel(self.sub_canvas))
        
        self._load_menu_items()
        
        self.menu_profile_label = tk.Label(self.background_label, bg="lightgrey", relief="solid", bd=1, text="Pic", font=("Arial", 8))
        self.menu_table_display_label = tk.Label(self.background_label, textvariable=self.current_table_name_var, 
                                                 font=("Arial", 16, "bold"), bg="white", fg="#D9534F")
        
        self.main_canvas.bind('<Configure>', self._on_resize_food_menu)
        self.after(100, lambda: self._on_resize_food_menu(None))

    # 🟢 (แก้ไข) เอา Description ออก
    def _load_menu_items(self):
        self.menu_image_references = []
        current_category = None
        
        for widget in self.menu_items_frame.winfo_children():
            widget.destroy()
            
        grid_container = tk.Frame(self.menu_items_frame, bg="#FEFEFE")
        grid_container.pack(fill="both", expand=True, padx=10, pady=10)

        max_cols = 2 
        current_col = 0
        current_row = 0

        for i in range(max_cols):
            grid_container.grid_columnconfigure(i, weight=1)

        current_category = None
        for item in MENU_DATA:
            if item["category"] != current_category:
                current_category = item["category"]
                
                if current_col != 0:
                    current_col = 0
                    current_row += 1
                    
                category_label = tk.Label(grid_container, text=current_category.upper(),
                                        font=("Arial", 18, "bold"), bg="#E0E0E0", fg="#333333", anchor="w")
                category_label.grid(row=current_row, column=0, columnspan=max_cols, sticky="ew", pady=(20, 5), padx=10)
                
                current_row += 1 
                current_col = 0 
                
            item_frame = tk.Frame(grid_container, bg="#FEFEFE", relief="solid", bd=1)
            
            image_label = tk.Label(item_frame, bg="white", text="No Img", 
                                   width=FOOD_ITEM_IMAGE_WIDTH, height=FOOD_ITEM_IMAGE_HEIGHT) 
            image_label.pack(side="left", padx=10, pady=10) 
            
            try:
                img_path = os.path.join(BASE_DIR, item["image"])
                if os.path.exists(img_path):
                    img = Image.open(img_path)
                    img.thumbnail((FOOD_ITEM_IMAGE_WIDTH, FOOD_ITEM_IMAGE_HEIGHT), Image.Resampling.LANCZOS) 
                    img_tk = ImageTk.PhotoImage(img)
                    image_label.config(image=img_tk, width=FOOD_ITEM_IMAGE_WIDTH, height=FOOD_ITEM_IMAGE_HEIGHT) 
                    self.menu_image_references.append(img_tk)
                else:
                    print(f"🟠 WARNING: ไม่พบรูปเมนู '{item['image']}' ที่ {BASE_DIR}")
            except Exception as e:
                print(f"🔴 ERROR loading image {item['image']}: {e}")
                
            
            text_frame = tk.Frame(item_frame, bg="#FEFEFE")
            text_frame.pack(side="left", expand=True, fill="both", padx=10, pady=10) 

            name_label = tk.Label(text_frame, text=item["name"], 
                                  font=("Arial", 16, "bold"), bg="#FEFEFE", anchor="w")
            name_label.pack(fill="x", pady=(5, 0))

            # 🟢 (ลบ) ลบส่วน Description ออก
            
            add_button = tk.Button(item_frame, text="  +  ", font=("Arial", 16, "bold"), 
                                   command=lambda name=item["name"]: self.prompt_for_quantity(name), 
                                   bg="#2ECC71", fg="white", relief="flat")
            add_button.pack(side="right", padx=10, pady=10)

            item_frame.grid(row=current_row, column=current_col, padx=10, pady=5, sticky="nsew")

            click_callback = lambda event, name=item["name"]: self.prompt_for_quantity(name)
            item_frame.bind("<Button-1>", click_callback)
            image_label.bind("<Button-1>", click_callback)
            text_frame.bind("<Button-1>", click_callback)
            name_label.bind("<Button-1>", click_callback)
            # description_label.bind("<Button-1>", click_callback) # 🟢 (ลบ)

            current_col += 1
            if current_col >= max_cols:
                current_col = 0
                current_row += 1

    def _on_resize_food_menu(self, event):
        bg_image, tk_image_attr = self.original_food_menu_image, 'food_menu_bg_image_tk'
        if not bg_image: return
        canvas_width = self.main_canvas.winfo_width()
        if canvas_width < 50: return
        
        try:
            orig_width, orig_height = bg_image.size
            if orig_width == 0: return
            
            scale_factor = canvas_width / float(orig_width); self.current_scale_factor = scale_factor
            target_width, target_height = canvas_width, int(orig_height * scale_factor)
            
            resized_img = bg_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            setattr(self, tk_image_attr, ImageTk.PhotoImage(resized_img))
            self.background_label.config(image=getattr(self, tk_image_attr), width=target_width, height=target_height)
            self.background_label.pack_configure(expand=True, fill='both')
            
            menu_x1 = int(MENU_SUB_FRAME_REGION["x_start"] * scale_factor)
            menu_y1 = int(MENU_SUB_FRAME_REGION["y_start"] * scale_factor)
            menu_w = int((MENU_SUB_FRAME_REGION["x_end"] - MENU_SUB_FRAME_REGION["x_start"]) * scale_factor)
            
            menu_h = target_height - menu_y1 - int(20 * scale_factor) 
            
            if menu_h < 100: menu_h = 100 
            
            if hasattr(self, 'sub_canvas_scrollbar') and hasattr(self, 'sub_canvas'):
                scrollbar_width = 16
                canvas_w = menu_w - scrollbar_width
                
                self.sub_canvas.place(in_=self.background_label, x=menu_x1, y=menu_y1, width=canvas_w, height=menu_h)
                self.sub_canvas_scrollbar.place(in_=self.background_label, x=menu_x1 + canvas_w, y=menu_y1, width=scrollbar_width, height=menu_h)
            
            self.sub_canvas.config(scrollregion=self.sub_canvas.bbox("all"))

            if hasattr(self, 'menu_profile_label'):
                w, h = self._place_and_scale_widget(self.menu_profile_label, ORIG_MENU_PROFILE_BOX, scale_factor, self.background_label)
                if self.current_user_profile_path:
                    self.load_menu_profile_image_resized(self.current_user_profile_path, (w, h))

            if hasattr(self, 'menu_table_display_label'):
                self._place_and_scale_widget(self.menu_table_display_label, ORIG_MENU_TABLE_LABEL, scale_factor, self.background_label, is_label=True, bold=True)
                
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
                                        
        except Exception as e: print(f"🔴 ERROR in _on_resize_food_menu: {e}")

    # --- หน้ารายการสั่งซื้อ (Order List) ---
    def show_order_list_screen(self):
        self.main_canvas = self._create_canvas_with_scrollbar(self.content_frame)
        frame_bg = "#B32415"
        self.scrollable_frame_order = self._setup_scrollable_frame(self.main_canvas, frame_bg)
        self.background_label = tk.Label(self.scrollable_frame_order, image=None, borderwidth=0, bg=frame_bg)
        self.background_label.pack(); self.background_label.bind('<Button-1>', self.get_click_position)
        self.order_text_box = tk.Text(self.background_label, font=("Tahoma", 12), bg=frame_bg, fg="white", bd=0, relief="flat", wrap="word", state="disabled")
        self.main_canvas.bind('<Configure>', self._on_resize_order_list)
        self.after(100, lambda: self._on_resize_order_list(None))
        self.after(110, self.update_order_list_display)

    def _on_resize_order_list(self, event):
        bg_image, tk_image_attr = self.original_order_list_image, 'order_list_bg_image_tk'
        if not bg_image: return
        canvas_width = self.main_canvas.winfo_width()
        if canvas_width < 50: return
        try:
            orig_width, orig_height = bg_image.size
            if orig_width == 0: return
            scale_factor = canvas_width / float(orig_width); self.current_scale_factor = scale_factor
            target_width, target_height = canvas_width, int(orig_height * scale_factor)
            resized_img = bg_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            setattr(self, tk_image_attr, ImageTk.PhotoImage(resized_img))
            self.background_label.config(image=getattr(self, tk_image_attr), width=target_width, height=target_height)
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
            if hasattr(self, 'order_text_box'):
                                    _, th = self._place_and_scale_widget(self.order_text_box,
                                                 {"x": ORIG_TEXTBOX_X, "y": ORIG_TEXTBOX_Y, "width": ORIG_TEXTBOX_W, "height": ORIG_TEXTBOX_H},
                                                 scale_factor, self.background_label)
                                    font_size = max(8, int(th * 0.04))
                                    self.order_text_box.config(font=("Tahoma", font_size))
        except Exception as e: print(f"🔴 ERROR in _on_resize_order_list: {e}")

    def update_order_list_display(self):
        if not hasattr(self, 'order_text_box'): return
        self.order_text_box.config(state="normal")
        self.order_text_box.delete("1.0", "end")
        
        items_to_display = []
        
        for item_spec in MENU_DATA:
            item_name = item_spec["name"]
            
            if self.cart.get(item_name, 0) > 0:
                qty = self.cart[item_name]
                items_to_display.append({
                    "name": item_name,
                    "qty": qty
                })

        if not items_to_display: 
            self.order_text_box.insert("end", "🛒 ตะกร้าของคุณว่างเปล่า")
        else:
            self.order_text_box.config(tabs=(300)) 
            
            self.order_text_box.tag_configure("header", font=("Tahoma", 14, "bold"), underline=True)
            self.order_text_box.tag_configure("item", font=("Tahoma", 12))

            display_string = " รายการ\t\tจำนวน\n"
            self.order_text_box.insert("end", display_string, "header")
            self.order_text_box.insert("end", "-"*60 + "\n\n")

            item_number = 1
            for item in items_to_display:
                display_string = f" {item_number}. {item['name']}\t\t{item['qty']} ชิ้น\n"
                self.order_text_box.insert("end", display_string, "item")
                item_number += 1

        self.order_text_box.config(state="disabled")

    def show_summary_page(self):
        self.main_canvas = self._create_canvas_with_scrollbar(self.content_frame)
        frame_bg = "#E0E0E0"
        self.scrollable_frame_summary = self._setup_scrollable_frame(self.main_canvas, frame_bg)
        self.background_label = tk.Label(self.scrollable_frame_summary, image=None, borderwidth=0, bg=frame_bg)
        self.background_label.pack(); self.background_label.bind('<Button-1>', self.get_click_position)
        
        self.summary_text_label = tk.Label(self.background_label, text="นี่คือหน้ารวมสำหรับ Staff", 
                                           font=("Arial", 20, "bold"), bg="white", fg="black")
        
        self.main_canvas.bind('<Configure>', self._on_resize_summary_page)
        self.after(100, lambda: self._on_resize_summary_page(None))

    def _on_resize_summary_page(self, event):
        bg_image, tk_image_attr = self.original_summary_page_image, 'summary_bg_image_tk'
        if not bg_image: 
            print("🔴 WARNING: ไม่พบไฟล์ 'หน้ารวม.png' สำหรับ 'summary_page_bg'")
            return
        canvas_width = self.main_canvas.winfo_width()
        if canvas_width < 50: return
        try:
            orig_width, orig_height = bg_image.size; scale_factor = canvas_width / float(orig_width)
            self.current_scale_factor = scale_factor
            target_width, target_height = canvas_width, int(orig_height * scale_factor)
            resized_img = bg_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            setattr(self, tk_image_attr, ImageTk.PhotoImage(resized_img))
            self.background_label.config(image=getattr(self, tk_image_attr), width=target_width, height=target_height)
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

            if hasattr(self, 'summary_text_label'):
                x_center = (orig_width / 2) * scale_factor
                y_center = (orig_height / 2) * scale_factor
                self.summary_text_label.place(x=x_center, y=y_center, anchor="center")
                
        except Exception as e: print(f"🔴 ERROR in _on_resize_summary_page: {e}")


    # --- หน้าลงทะเบียน (Register) ---
    def show_register_page(self):
        self.main_canvas = self._create_canvas_with_scrollbar(self.content_frame)
        frame_bg = "#FFFFFF"; widget_bg="#F0F0F0"
        self.scrollable_frame_register = self._setup_scrollable_frame(self.main_canvas, frame_bg)
        self.background_label = tk.Label(self.scrollable_frame_register, image=None, borderwidth=0, bg=frame_bg)
        self.background_label.pack(); self.background_label.bind('<Button-1>', self.get_click_position)
        self.reg_username_label = tk.Label(self.background_label, text="ชื่อผู้ใช้:", font=("Arial", 10,"bold"), bg=widget_bg, anchor="w")
        self.reg_password1_label = tk.Label(self.background_label, text="รหัสผ่าน:", font=("Arial", 10,"bold"), bg=widget_bg, anchor="w")
        self.reg_password2_label = tk.Label(self.background_label, text="ยืนยันรหัสผ่าน:", font=("Arial", 10,"bold"), bg=widget_bg, anchor="w")
        self.reg_phone_label = tk.Label(self.background_label, text="เบอร์โทร:", font=("Arial", 10,"bold"), bg=widget_bg, anchor="w")
        self.reg_email_label = tk.Label(self.background_label, text="อีเมล:", font=("Arial", 10,"bold"), bg=widget_bg, anchor="w")
        self.reg_username_entry = tk.Entry(self.background_label, textvariable=self.reg_username_var, font=("Arial", 12), relief="flat", bd=0, bg=widget_bg)
        self.reg_password1_entry = tk.Entry(self.background_label, textvariable=self.reg_password1_var, font=("Arial", 12), show="*", relief="flat", bd=0, bg=widget_bg)
        self.reg_password2_entry = tk.Entry(self.background_label, textvariable=self.reg_password2_var, font=("Arial", 12), show="*", relief="flat", bd=0, bg=widget_bg)
        self.reg_phone_entry = tk.Entry(self.background_label, textvariable=self.reg_phone_var, font=("Arial", 12), relief="flat", bd=0, bg=widget_bg)
        self.reg_email_entry = tk.Entry(self.background_label, textvariable=self.reg_email_var, font=("Arial", 12), relief="flat", bd=0, bg=widget_bg)
        
        self.reg_profile_label = tk.Label(self.background_label, text="", relief="solid", bd=1, bg="lightgrey")
        self.reg_profile_label.bind('<Button-1>', self.select_profile_image)
        
        self.main_canvas.bind('<Configure>', self._on_resize_register_page)
        self.after(100, lambda: self._on_resize_register_page(None))

    def _on_resize_register_page(self, event):
        bg_image, tk_image_attr = self.original_register_image, 'register_bg_image_tk'
        if not bg_image: return
        canvas_width = self.main_canvas.winfo_width()
        if canvas_width < 50: return
        try:
            orig_width, orig_height = bg_image.size; scale_factor = canvas_width / float(orig_width)
            self.current_scale_factor = scale_factor
            target_width, target_height = canvas_width, int(orig_height * scale_factor)
            resized_img = bg_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            setattr(self, tk_image_attr, ImageTk.PhotoImage(resized_img))
            self.background_label.config(image=getattr(self, tk_image_attr), width=target_width, height=target_height)
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

            self._place_and_scale_widget(self.reg_username_label, ORIG_REG_USERNAME_LABEL, scale_factor, self.background_label, is_label=True, bold=True)
            self._place_and_scale_widget(self.reg_password1_label, ORIG_REG_PASSWORD1_LABEL, scale_factor, self.background_label, is_label=True, bold=True)
            self._place_and_scale_widget(self.reg_password2_label, ORIG_REG_PASSWORD2_LABEL, scale_factor, self.background_label, is_label=True, bold=True)
            self._place_and_scale_widget(self.reg_phone_label, ORIG_REG_PHONE_LABEL, scale_factor, self.background_label, is_label=True, bold=True)
            self._place_and_scale_widget(self.reg_email_label, ORIG_REG_EMAIL_LABEL, scale_factor, self.background_label, is_label=True, bold=True)
            self._place_and_scale_widget(self.reg_username_entry, ORIG_REG_USERNAME_BOX, scale_factor, self.background_label)
            self._place_and_scale_widget(self.reg_password1_entry, ORIG_REG_PASSWORD1_BOX, scale_factor, self.background_label)
            self._place_and_scale_widget(self.reg_password2_entry, ORIG_REG_PASSWORD2_BOX, scale_factor, self.background_label)
            self._place_and_scale_widget(self.reg_phone_entry, ORIG_REG_PHONE_BOX, scale_factor, self.background_label)
            self._place_and_scale_widget(self.reg_email_entry, ORIG_REG_EMAIL_BOX, scale_factor, self.background_label)

            if hasattr(self, 'reg_profile_label'):
                pw, ph = self._place_and_scale_widget(self.reg_profile_label, ORIG_REG_PROFILE_BOX, scale_factor, self.background_label)
                if self.selected_profile_image_path and pw > 0 and ph > 0:
                    self.load_register_profile_preview(self.selected_profile_image_path, (pw, ph))
                elif ph > 0:
                    self.load_placeholder_image('reg_profile_label', 'placeholder_image_tk', (pw, ph))

        except Exception as e: print(f"🔴 ERROR in _on_resize_register_page: {e}")

    # --- หน้าลืมรหัสผ่าน (Forgot Password) ---
    def show_forgot_page(self):
        self.main_canvas = self._create_canvas_with_scrollbar(self.content_frame)
        frame_bg="#FFFFFF"; widget_bg="#F0F0F0"
        self.scrollable_frame_forgot = self._setup_scrollable_frame(self.main_canvas, frame_bg)
        self.background_label = tk.Label(self.scrollable_frame_forgot, image=None, borderwidth=0, bg=frame_bg)
        self.background_label.pack(); self.background_label.bind('<Button-1>', self.get_click_position)
        self.forgot_email_label = tk.Label(self.background_label, text="อีเมล:", font=("Arial", 10,"bold"), bg=widget_bg, anchor="w")
        self.forgot_phone_label = tk.Label(self.background_label, text="เบอร์โทร:", font=("Arial", 10,"bold"), bg=widget_bg, anchor="w")
        self.forgot_email_entry = tk.Entry(self.background_label, textvariable=self.forgot_email_var, font=("Arial", 12), relief="flat", bd=0, bg=widget_bg)
        self.forgot_phone_entry = tk.Entry(self.background_label, textvariable=self.forgot_phone_var, font=("Arial", 12), relief="flat", bd=0, bg=widget_bg)
        self.main_canvas.bind('<Configure>', self._on_resize_forgot_page)
        self.after(100, lambda: self._on_resize_forgot_page(None))

    def _on_resize_forgot_page(self, event):
        bg_image, tk_image_attr = self.original_forgot_image, 'forgot_bg_image_tk'
        if not bg_image: return
        canvas_width = self.main_canvas.winfo_width()
        if canvas_width < 50: return
        try:
            orig_width, orig_height = bg_image.size; scale_factor = canvas_width / float(orig_width)
            self.current_scale_factor = scale_factor
            target_width, target_height = canvas_width, int(orig_height * scale_factor)
            resized_img = bg_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            setattr(self, tk_image_attr, ImageTk.PhotoImage(resized_img))
            self.background_label.config(image=getattr(self, tk_image_attr), width=target_width, height=target_height)
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
            self._place_and_scale_widget(self.forgot_email_label, ORIG_FORGOT_EMAIL_LABEL, scale_factor, self.background_label, is_label=True, bold=True)
            self._place_and_scale_widget(self.forgot_phone_label, ORIG_FORGOT_PHONE_LABEL, scale_factor, self.background_label, is_label=True, bold=True)
            self._place_and_scale_widget(self.forgot_email_entry, ORIG_FORGOT_EMAIL_BOX, scale_factor, self.background_label)
            self._place_and_scale_widget(self.forgot_phone_entry, ORIG_FORGOT_PHONE_BOX, scale_factor, self.background_label)
        except Exception as e: print(f"🔴 ERROR in _on_resize_forgot_page: {e}")

    # 🟢 (แก้ไข) หน้า Admin Edit - เปลี่ยนเป็นหน้า "จัดการโต๊ะ" (UI ใหม่)
    def show_admin_edit_page(self):
        self.main_canvas = self._create_canvas_with_scrollbar(self.content_frame)
        frame_bg="#ADD8E6"
        self.scrollable_frame_admin = self._setup_scrollable_frame(self.main_canvas, frame_bg)
        self.background_label = tk.Label(self.scrollable_frame_admin, image=None, borderwidth=0, bg=frame_bg)
        self.background_label.pack(); self.background_label.bind('<Button-1>', self.get_click_position)

        # 🟢 (เพิ่ม) สร้างป้ายสถานะโต๊ะ (เหมือนหน้า table_page)
        self.table_status_labels_admin_page = [
            tk.Label(self.background_label, text="", font=("Arial", 10, "bold"), bg=frame_bg) 
            for _ in TABLE_CENTERS
        ]
        
        self.main_canvas.bind('<Configure>', self._on_resize_admin_edit_page)
        self.after(100, lambda: self._on_resize_admin_edit_page(None))

    def _on_resize_admin_edit_page(self, event):
        bg_image, tk_image_attr = self.original_admin_edit_image, 'admin_edit_bg_image_tk' 
        if not bg_image: return
        
        canvas_width = self.main_canvas.winfo_width()
        if canvas_width < 50: return
        
        try:
            orig_width, orig_height = bg_image.size; scale_factor = canvas_width / float(orig_width)
            self.current_scale_factor = scale_factor
            target_width, target_height = canvas_width, int(orig_height * scale_factor)
            resized_img = bg_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            setattr(self, tk_image_attr, ImageTk.PhotoImage(resized_img))
            self.background_label.config(image=getattr(self, tk_image_attr), width=target_width, height=target_height)
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
            
            # 🟢 (เพิ่ม) วางป้ายสถานะโต๊ะ (เหมือน _on_resize_table_page)
            for i, label in enumerate(self.table_status_labels_admin_page):
                if i < len(TABLE_REGIONS) and i < len(TABLE_ALIGNMENT_CENTERS):
                    align_coords = TABLE_ALIGNMENT_CENTERS[i]
                    
                    font_size = max(6, int(TABLE_CLICK_HEIGHT * scale_factor * 0.3))
                    label.config(font=("Arial", font_size, "bold"), bg='white')
                    orig_corner_x = align_coords["x"] + table_half_w
                    orig_corner_y = align_coords["y"] - table_half_h
                    corner_x = int(orig_corner_x * scale_factor)
                    corner_y = int(orig_corner_y * scale_factor)
                    
                    # (ตั้งค่าสีตามสถานะ)
                    if self.table_status[i] == 'occupied':
                        label.config(text="\u2717", fg="#E74C3C") # ✗ (แดง)
                    else:
                        label.config(text="\u2713", fg="#2ECC71") # ✓ (เขียว)
                    
                    label.place(x=corner_x, y=corner_y, anchor="c")
                else:
                    label.place_forget()

        except Exception as e: print(f"🔴 ERROR in _on_resize_admin_edit_page: {e}")

# --- หน้าจอแสดงโปรไฟล์ (Profile Display) ---
    def show_profile_page(self):
        self.main_canvas = self._create_canvas_with_scrollbar(self.content_frame)
        frame_bg = "#E8F8F5"; widget_bg="#F0F0F0"
        self.scrollable_frame_profile = self._setup_scrollable_frame(self.main_canvas, frame_bg)
        self.background_label = tk.Label(self.scrollable_frame_profile, image=None, borderwidth=0, bg=frame_bg)
        self.background_label.pack(); self.background_label.bind('<Button-1>', self.get_click_position)

        self.profile_username_label = tk.Label(self.background_label, text="ชื่อผู้ใช้:", font=("Arial", 10,"bold"), bg=widget_bg, anchor="w")
        self.profile_phone_label    = tk.Label(self.background_label, text="เบอร์โทร:", font=("Arial", 10,"bold"), bg=widget_bg, anchor="w")
        self.profile_email_label    = tk.Label(self.background_label, text="อีเมล:", font=("Arial", 10,"bold"), bg=widget_bg, anchor="w")
        self.profile_password_label = tk.Label(self.background_label, text="รหัสผ่าน:", font=("Arial", 10,"bold"), bg=widget_bg, anchor="w") 

        self.profile_username_display = tk.Entry(self.background_label, textvariable=self.profile_display_username, font=("Arial", 12), relief="flat", bd=0, bg=widget_bg, state='readonly', readonlybackground=widget_bg)
        self.profile_phone_display    = tk.Entry(self.background_label, textvariable=self.profile_display_phone,    font=("Arial", 12), relief="flat", bd=0, bg=widget_bg, state='readonly', readonlybackground=widget_bg)
        self.profile_email_display    = tk.Entry(self.background_label, textvariable=self.profile_display_email,    font=("Arial", 12), relief="flat", bd=0, bg=widget_bg, state='readonly', readonlybackground=widget_bg)
        self.profile_password_display = tk.Entry(self.background_label, textvariable=self.profile_display_password, font=("Arial", 12), relief="flat", bd=0, bg=widget_bg, state='readonly', readonlybackground=widget_bg, show="*") 

        self.profile_image_label = tk.Label(self.background_label, bg="lightgrey", relief="solid", bd=1, text="Profile")

        self.profile_display_username.set(self.lookup_user_data.get("username", "N/A"))
        self.profile_display_phone.set(self.lookup_user_data.get("phone", "N/A"))
        self.profile_display_email.set(self.lookup_user_data.get("email", "N/A"))
        self.profile_display_password.set(self.lookup_user_data.get("password", "N/A")) 

        self.main_canvas.bind('<Configure>', self._on_resize_profile_page)
        self.after(100, lambda: self._on_resize_profile_page(None))
        self.after(110, lambda: self.toggle_profile_edit_mode(False)) 

    def _on_resize_profile_page(self, event):
        bg_image, tk_image_attr = self.original_profile_page_image, 'profile_page_bg_image_tk'
        if not bg_image: return
        canvas_width = self.main_canvas.winfo_width()
        if canvas_width < 50: return
        try:
            orig_width, orig_height = bg_image.size; scale_factor = canvas_width / float(orig_width)
            self.current_scale_factor = scale_factor
            target_width, target_height = canvas_width, int(orig_height * scale_factor)
            resized_img = bg_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            setattr(self, tk_image_attr, ImageTk.PhotoImage(resized_img))
            self.background_label.config(image=getattr(self, tk_image_attr), width=target_width, height=target_height)
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

            self._place_and_scale_widget(self.profile_username_label, ORIG_PROFILE_USERNAME_LABEL, scale_factor, self.background_label, is_label=True, bold=True)
            self._place_and_scale_widget(self.profile_username_display, ORIG_PROFILE_USERNAME_DISPLAY, scale_factor, self.background_label)
            
            self._place_and_scale_widget(self.profile_phone_label, ORIG_PROFILE_PHONE_LABEL, scale_factor, self.background_label, is_label=True, bold=True)
            self._place_and_scale_widget(self.profile_phone_display, ORIG_PROFILE_PHONE_DISPLAY, scale_factor, self.background_label)
            
            self._place_and_scale_widget(self.profile_email_label, ORIG_PROFILE_EMAIL_LABEL, scale_factor, self.background_label, is_label=True, bold=True)
            self._place_and_scale_widget(self.profile_email_display, ORIG_PROFILE_EMAIL_DISPLAY, scale_factor, self.background_label)

            self._place_and_scale_widget(self.profile_password_label, ORIG_PROFILE_PASSWORD_LABEL, scale_factor, self.background_label, is_label=True, bold=True)
            self._place_and_scale_widget(self.profile_password_display, ORIG_PROFILE_PASSWORD_DISPLAY, scale_factor, self.background_label)

            if hasattr(self, 'profile_image_label'):
                pw, ph = self._place_and_scale_widget(self.profile_image_label, ORIG_PROFILE_IMAGE_BOX, scale_factor, self.background_label)
                if self.lookup_user_data.get("profile_image_path") and pw > 0 and ph > 0:
                    self.load_profile_page_image_resized(self.lookup_user_data["profile_image_path"], (pw, ph))
                elif ph > 0:
                    font_size = max(6, int(ph * 0.15))
                    self.profile_image_label.config(image=None, text="No Pic", font=("Arial", font_size))

        except Exception as e: print(f"🔴 ERROR in _on_resize_profile_page: {e}")
        
    # ----------------------------------------------------------------------
    # 🟢 START: (แก้ไข) หน้า "เพิ่มสินค้า" (ลบช่อง ราคา)
    # ----------------------------------------------------------------------
    def show_add_item_page(self):
        self.main_canvas = self._create_canvas_with_scrollbar(self.content_frame)
        frame_bg="#FFFFFF"; widget_bg="#F0F0F0"
        self.scrollable_frame_add_item = self._setup_scrollable_frame(self.main_canvas, frame_bg)
        self.background_label = tk.Label(self.scrollable_frame_add_item, image=None, borderwidth=0, bg=frame_bg)
        self.background_label.pack(); self.background_label.bind('<Button-1>', self.get_click_position)

        self.add_item_image_label = tk.Label(self.background_label, text="", relief="solid", bd=1, bg="lightgrey")
        self.add_item_image_label.bind('<Button-1>', self.select_add_item_image)
        
        self.add_item_name_label = tk.Label(self.background_label, text="ชื่อสินค้า:", font=("Arial", 10,"bold"), bg=widget_bg, anchor="w")
        self.add_item_name_entry = tk.Entry(self.background_label, textvariable=self.add_item_name_var, font=("Arial", 12), relief="flat", bd=0, bg=widget_bg)
        
        self.add_item_cat_label = tk.Label(self.background_label, text="ประเภท:", font=("Arial", 10,"bold"), bg=widget_bg, anchor="w")
        
        self.add_item_cat_optionmenu = tk.OptionMenu(self.background_label, self.add_item_category_var, *CATEGORY_OPTIONS) 
        self.add_item_cat_optionmenu.config(font=("Arial", 12), relief="flat", bd=0, bg=widget_bg, activebackground=widget_bg, highlightthickness=0, anchor='w')
        self.add_item_cat_optionmenu['menu'].config(font=("Arial", 12), bg=widget_bg)

        # (ลบ Price Widgets)

        self.main_canvas.bind('<Configure>', self._on_resize_add_item_page)
        self.after(100, lambda: self._on_resize_add_item_page(None))

    def _on_resize_add_item_page(self, event):
        bg_image, tk_image_attr = self.original_add_item_page_image, 'add_item_bg_image_tk'
        if not bg_image: 
            print("🔴 WARNING: ไม่พบไฟล์ 'หน้าเพิ่ม.png' สำหรับ 'add_item_page_bg'")
            return
        canvas_width = self.main_canvas.winfo_width()
        if canvas_width < 50: return
        try:
            orig_width, orig_height = bg_image.size; scale_factor = canvas_width / float(orig_width)
            self.current_scale_factor = scale_factor
            target_width, target_height = canvas_width, int(orig_height * scale_factor)
            resized_img = bg_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            setattr(self, tk_image_attr, ImageTk.PhotoImage(resized_img))
            self.background_label.config(image=getattr(self, tk_image_attr), width=target_width, height=target_height)
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

            self._place_and_scale_widget(self.add_item_name_label, ORIG_ADD_ITEM_NAME_LABEL, scale_factor, self.background_label, is_label=True, bold=True)
            self._place_and_scale_widget(self.add_item_name_entry, ORIG_ADD_ITEM_NAME_BOX, scale_factor, self.background_label)
            self._place_and_scale_widget(self.add_item_cat_label, ORIG_ADD_ITEM_CAT_LABEL, scale_factor, self.background_label, is_label=True, bold=True)
            
            _, h = self._place_and_scale_widget(self.add_item_cat_optionmenu, ORIG_ADD_ITEM_CAT_BOX, scale_factor, self.background_label)
            font_size = max(6, int(h * 0.4)) 
            self.add_item_cat_optionmenu.config(font=("Arial", font_size))
            if hasattr(self, 'add_item_cat_optionmenu') and 'menu' in self.add_item_cat_optionmenu.cget('menu'):
                       self.add_item_cat_optionmenu['menu'].config(font=("Arial", font_size))

            # (ลบ Price Widgets)

            if hasattr(self, 'add_item_image_label'):
                pw, ph = self._place_and_scale_widget(self.add_item_image_label, ORIG_ADD_ITEM_IMAGE_BOX, scale_factor, self.background_label)
                if self.add_item_image_path and pw > 0 and ph > 0:
                    self.load_add_item_image_preview(self.add_item_image_path, (pw, ph))
                elif ph > 0:
                    self.load_placeholder_image('add_item_image_label', 'placeholder_image_tk', (pw, ph))

        except Exception as e: print(f"🔴 ERROR in _on_resize_add_item_page: {e}")
    # ----------------------------------------------------------------------
    # 🟢 END: (แก้ไข)
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # 🟢 START: (แก้ไข) หน้า Order Status
    # ----------------------------------------------------------------------
    def show_order_status_page(self):
        self.main_canvas = self._create_canvas_with_scrollbar(self.content_frame)
        frame_bg = "#B32415" 
        self.scrollable_frame_order_status = self._setup_scrollable_frame(self.main_canvas, frame_bg)
        
        self.background_label = tk.Label(self.scrollable_frame_order_status, image=None, borderwidth=0, bg=frame_bg)
        self.background_label.pack(); 
        self.background_label.bind('<Button-1>', self.get_click_position)

        self.order_status_text_box = tk.Text(self.background_label, font=("Tahoma", 14), 
                                             bg="#FFFFFF", fg="black", bd=0, relief="flat", 
                                             wrap="word", state="disabled")

        self.main_canvas.bind('<Configure>', self._on_resize_order_status_page)
        self.after(100, lambda: self._on_resize_order_status_page(None))
        self.after(110, self.load_order_statuses) 

    def _on_resize_order_status_page(self, event):
        bg_image, tk_image_attr = self.original_order_status_page_image, 'order_status_bg_image_tk'
        if not bg_image: return
        canvas_width = self.main_canvas.winfo_width()
        if canvas_width < 50: return
        try:
            orig_width, orig_height = bg_image.size
            if orig_width == 0: return
            scale_factor = canvas_width / float(orig_width); self.current_scale_factor = scale_factor
            target_width, target_height = canvas_width, int(orig_height * scale_factor)
            
            resized_img = bg_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
            setattr(self, tk_image_attr, ImageTk.PhotoImage(resized_img))
            self.background_label.config(image=getattr(self, tk_image_attr), width=target_width, height=target_height)
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

            if hasattr(self, 'order_status_text_box'):
                                _, th = self._place_and_scale_widget(self.order_status_text_box,
                                                 ORIG_ORDER_STATUS_BOX,
                                                 scale_factor, self.background_label)
                                # 🟢 (แก้ไข) เพิ่มขนาด Font
                                font_size = max(10, int(th * 0.035)) 
                                self.order_status_text_box.config(font=("Tahoma", font_size))
                                
        except Exception as e: print(f"🔴 ERROR in _on_resize_order_status_page: {e}")

    # 🟢 (แก้ไข) แก้ไขเวลา + ขนาดตัวอักษร
    def load_order_statuses(self):
        """Fetches pending orders from DB and displays them grouped by table."""
        if not hasattr(self, 'order_status_text_box'): return
        
        self.order_status_text_box.config(state="normal")
        self.order_status_text_box.delete("1.0", "end")

        orders_by_table = defaultdict(lambda: defaultdict(list))
        order_times = {} # 🟢 NEW: Store time
        conn = None
        try:
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()
            
            query = """
                SELECT o.table_name, o.order_id, o.order_time, m.item_name, m.quantity
                FROM Orders o
                JOIN Menu m ON o.order_id = m.order_id
                WHERE o.status = 'pending'
                ORDER BY o.table_name, o.order_id;
            """
            cursor.execute(query)
            all_items = cursor.fetchall()
            
            if not all_items:
                self.order_status_text_box.insert("end", "ไม่มีรายการสั่งซื้อที่ค้างอยู่...")
                self.order_status_text_box.config(state="disabled")
                return

            # จัดกลุ่มข้อมูล
            for table, order_id, order_time, item, qty in all_items:
                orders_by_table[table][order_id].append(f"  - {item} x {qty}")
                if order_id not in order_times:
                    # 🟢 (แก้ไข) แปลงเวลา + บวก 7 ชั่วโมง (เวลาไทย)
                    try:
                        # (Format: 2025-11-09 14:45:00) - SQLite/UTC
                        dt_utc = datetime.datetime.fromisoformat(order_time)
                        dt_thai = dt_utc + timedelta(hours=7)
                        # (Format: 09/11/2025 21:45:00) - Thai
                        time_str = dt_thai.strftime("%d/%m/%Y %H:%M:%S")
                    except Exception as e:
                        print(f"Error parsing time: {e}")
                        time_str = order_time # Fallback
                    order_times[order_id] = time_str

            # 🟢 (แก้ไข) ตั้งค่า Tags (เพิ่มขนาด)
            self.order_status_text_box.tag_configure("table_header", font=("Tahoma", 18, "bold"), spacing3=10, underline=True)
            self.order_status_text_box.tag_configure("order_header", font=("Tahoma", 16, "italic"), lmargin1=10, spacing1=5)
            self.order_status_text_box.tag_configure("item", font=("Tahoma", 16), spacing1=5, lmargin1=25)
            
            # แสดงผล
            for table_name, orders in orders_by_table.items():
                self.order_status_text_box.insert("end", f"{table_name}:\n", "table_header")
                
                for order_id, items in orders.items():
                    time_str = order_times.get(order_id, "N/A")
                    self.order_status_text_box.insert("end", f" Order #{order_id} (เวลา: {time_str})\n", "order_header")
                    self.order_status_text_box.insert("end", "\n".join(items) + "\n\n", "item")

        except sqlite3.Error as e:
            self.order_status_text_box.insert("end", f"เกิดข้อผิดพลาดในการโหลดข้อมูล: {e}")
        finally:
            if conn: conn.close()
            self.order_status_text_box.config(state="disabled")
    # ----------------------------------------------------------------------
    # 🟢 END: (แก้ไข)
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
    # 🟢 START: (แก้ไข) หน้าเงิน (ปรับแก้)
    # ----------------------------------------------------------------------
    def show_money_page(self):
        self.main_canvas = self._create_canvas_with_scrollbar(self.content_frame)
        frame_bg = "#CCCCCC" # (สีเทา ถ้าไม่มีรูป)
        
        if self.original_money_page_image:
            frame_bg = "#FFFFFF" # (หรือสีที่เข้ากับรูป)
            
        self.scrollable_frame_money = self._setup_scrollable_frame(self.main_canvas, frame_bg)
        
        self.background_label = tk.Label(self.scrollable_frame_money, image=None, borderwidth=0, bg=frame_bg)
        self.background_label.pack(); 
        self.background_label.bind('<Button-1>', self.get_click_position)

        self.main_canvas.bind('<Configure>', self._on_resize_money_page)
        self.after(100, lambda: self._on_resize_money_page(None))

    def _on_resize_money_page(self, event):
        bg_image, tk_image_attr = self.original_money_page_image, 'money_page_bg_image_tk'
        
        canvas_width = self.main_canvas.winfo_width()
        if canvas_width < 50: return
        
        # (ถ้ามีรูป)
        if bg_image:
            try:
                orig_width, orig_height = bg_image.size
                if orig_width == 0: return
                scale_factor = canvas_width / float(orig_width); self.current_scale_factor = scale_factor
                target_width, target_height = canvas_width, int(orig_height * scale_factor)
                
                resized_img = bg_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
                setattr(self, tk_image_attr, ImageTk.PhotoImage(resized_img))
                self.background_label.config(image=getattr(self, tk_image_attr), width=target_width, height=target_height)
                self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
            except Exception as e: 
                print(f"🔴 ERROR in _on_resize_money_page (image load): {e}")
        
        # (ถ้าไม่มีรูป)
        else:
            self.current_scale_factor = 1.0 # (ตั้งค่าพื้นฐาน)
            bg_height = self.main_canvas.winfo_height()
            if bg_height < 50: bg_height = 800 # (ตั้งค่า default)
            self.background_label.config(image=None, width=canvas_width, height=bg_height)
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

    # ----------------------------------------------------------------------
    # 🟢 END: (แก้ไข)
    # ----------------------------------------------------------------------

    # ----------------------------------------------------------------------
# 🟢 START: (แก้ไขใหม่ทั้งหมด) หน้าบิล (Bill Page)
# ----------------------------------------------------------------------

    def show_bill_page(self):
        """ 🟢 (แก้ไขใหม่) แสดงหน้าบิล (หน้าสรุปยอด) """
        self.main_canvas = self._create_canvas_with_scrollbar(self.content_frame)
        frame_bg = "#FFFFFF" # (สีขาว)
        
        # (ตั้งค่าพื้นหลังตามรูป)
        if not self.original_bill_page_image:
            print("🔴 WARNING: ไม่พบ 'หน้าบิล.png', ใช้พื้นหลังสีขาวแทน")
            frame_bg = "#FFFFFF"
            
        self.scrollable_frame_bill = self._setup_scrollable_frame(self.main_canvas, frame_bg)
        
        self.background_label = tk.Label(self.scrollable_frame_bill, image=None, borderwidth=0, bg=frame_bg)
        self.background_label.pack(); 
        self.background_label.bind('<Button-1>', self.get_click_position)
        
        # --- 1. คำนวณค่าต่างๆ (VAT 7% Included) ---
        VAT_RATE = 0.07
        total_amount = self.final_bill_amount
        person_count = self.final_bill_person_count
        
        amount_before_vat = total_amount / (1 + VAT_RATE)
        vat_amount = total_amount - amount_before_vat

        self.bill_divider_var.set("-" * 80) 
        
        # --- 2. ตั้งค่า StringVars (🟢 แก้ไข: จัดชิดซ้าย-ขวา) ---
        
        self.bill_header_l1_var.set("Mooay Noi Shabu")
        self.bill_header_l2_var.set("246 หมู่ 3 ถ.มิตรภาพ ต.ศิลา")
        self.bill_header_l3_var.set("อ.เมือง จ.ขอนแก่น 40000")
        self.bill_header_l4_var.set("โทร. 0XX-XXX-XXXX | เลขประจำตัวผู้เสียภาษี: 0123456789012")
        
        RECEIPT_LINE_WIDTH = 48 
        LEFT_COL_WIDTH = 32     
        RIGHT_COL_WIDTH = 15    

        table_name = self.current_table_name_var.get() or "N/A"
        current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        self.bill_info_l1_var.set(f"โต๊ะ: {table_name} วันที่: {current_time}".ljust(RECEIPT_LINE_WIDTH)) 
        
        header_l = "รายการ (Description)"
        header_r = "จำนวนเงิน (Amount)"
        self.bill_body_header_var.set(f"{header_l.ljust(LEFT_COL_WIDTH)} {header_r.rjust(RIGHT_COL_WIDTH)}") 

        item_l = f"บุฟเฟ่ต์ชาบู ({person_count} ท่าน)"
        item_r = f"{total_amount:.2f}"
        self.bill_body_item_var.set(f"{item_l.ljust(LEFT_COL_WIDTH)} {item_r.rjust(RIGHT_COL_WIDTH)}") 

        sub_l = "ยอดรวม (Total):"
        sub_r = f"{amount_before_vat:.2f}"
        self.bill_subtotal_var.set(f"{sub_l.ljust(LEFT_COL_WIDTH)} {sub_r.rjust(RIGHT_COL_WIDTH)}") 

        vat_l = "ภาษีมูลค่าเพิ่ม (VAT 7%):"
        vat_r = f"{vat_amount:.2f}"
        self.bill_vat_var.set(f"{vat_l.ljust(LEFT_COL_WIDTH)} {vat_r.rjust(RIGHT_COL_WIDTH)}") 

        total_l = "ยอดสุทธิ (Grand Total):"
        total_r = f"{total_amount:.2f}"
        self.bill_total_var.set(f"{total_l.ljust(LEFT_COL_WIDTH)} {total_r.rjust(RIGHT_COL_WIDTH)}") 

        self.bill_footer1_var.set("(ชำระแล้วโดย QR Code)")
        self.bill_footer2_var.set("ขอบคุณที่มาอุดหนุนนะคะ 💖")

        # --- 3. สร้าง Labels ---
        align_center = "center" 
        align_receipt = "w"     
        
        header_font = ("Arial", 14, "bold")
        body_font = ("Arial", 11)
        
        receipt_font = ("Courier", 11) 
        receipt_font_bold = ("Courier", 11, "bold")
        receipt_total_font = ("Courier", 12, "bold")

        # (Header - ใช้ Arial / Center)
        self.bill_l1 = tk.Label(self.background_label, textvariable=self.bill_header_l1_var, font=("Arial", 18, "bold"), bg=frame_bg, anchor=align_center)
        self.bill_l2 = tk.Label(self.background_label, textvariable=self.bill_header_l2_var, font=body_font, bg=frame_bg, anchor=align_center)
        self.bill_l3 = tk.Label(self.background_label, textvariable=self.bill_header_l3_var, font=body_font, bg=frame_bg, anchor=align_center)
        self.bill_l4 = tk.Label(self.background_label, textvariable=self.bill_header_l4_var, font=body_font, bg=frame_bg, anchor=align_center)
        
        # (Receipt Body - ใช้ Courier / Left-aligned)
        self.bill_d1 = tk.Label(self.background_label, textvariable=self.bill_divider_var, font=receipt_font, bg=frame_bg, anchor=align_receipt)
        self.bill_info = tk.Label(self.background_label, textvariable=self.bill_info_l1_var, font=receipt_font, bg=frame_bg, anchor=align_receipt) 
        self.bill_d2 = tk.Label(self.background_label, textvariable=self.bill_divider_var, font=receipt_font, bg=frame_bg, anchor=align_receipt)
        
        self.bill_body_h = tk.Label(self.background_label, textvariable=self.bill_body_header_var, font=receipt_font_bold, bg=frame_bg, anchor=align_receipt) 
        self.bill_body_i = tk.Label(self.background_label, textvariable=self.bill_body_item_var, font=receipt_font, bg=frame_bg, anchor=align_receipt) 
        self.bill_d3 = tk.Label(self.background_label, textvariable=self.bill_divider_var, font=receipt_font, bg=frame_bg, anchor=align_receipt)

        self.bill_sub = tk.Label(self.background_label, textvariable=self.bill_subtotal_var, font=receipt_font, bg=frame_bg, anchor=align_receipt) 
        self.bill_vat = tk.Label(self.background_label, textvariable=self.bill_vat_var, font=receipt_font, bg=frame_bg, anchor=align_receipt) 
        self.bill_total = tk.Label(self.background_label, textvariable=self.bill_total_var, font=receipt_total_font, bg=frame_bg, anchor=align_receipt) 

        # (Footer - ใช้ Arial / Center)
        self.bill_f1 = tk.Label(self.background_label, textvariable=self.bill_footer1_var, font=body_font, bg=frame_bg, anchor=align_center)
        self.bill_f2 = tk.Label(self.background_label, textvariable=self.bill_footer2_var, font=header_font, bg=frame_bg, anchor=align_center)

        self.main_canvas.bind('<Configure>', self._on_resize_bill_page)
        self.after(100, lambda: self._on_resize_bill_page(None))

    def _on_resize_bill_page(self, event):
        """ 🟢 (แก้ไขใหม่) Resize สำหรับหน้าบิล (แก้บั๊กจัดกลาง) """
        bg_image, tk_image_attr = self.original_bill_page_image, 'bill_page_bg_image_tk'
        
        canvas_width = self.main_canvas.winfo_width()
        if canvas_width < 50: return
        
        effective_scale = 1.0
        orig_width = 1366 # (ใช้ค่าคงที่)

        if bg_image:
            try:
                orig_width, orig_height = bg_image.size
                if orig_width == 0: orig_width = 1366 # (ป้องกันหารด้วย 0)
                
                effective_scale = canvas_width / float(orig_width); self.current_scale_factor = effective_scale
                target_width, target_height = canvas_width, int(orig_height * effective_scale)
                
                resized_img = bg_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
                setattr(self, tk_image_attr, ImageTk.PhotoImage(resized_img))
                self.background_label.config(image=getattr(self, tk_image_attr), width=target_width, height=target_height)
                self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
            except Exception as e: 
                print(f"🔴 ERROR in _on_resize_bill_page (image load): {e}")
                bg_image = None # (บังคับให้ไปที่ else)
        
        if not bg_image: 
            effective_scale = canvas_width / float(orig_width) # ⭐️ (สำคัญ) คำนวณ scale โดยอิง 1366
            self.current_scale_factor = effective_scale
            
            bg_height = self.main_canvas.winfo_height()
            if bg_height < 50: bg_height = 800 
            self.background_label.config(image=None, width=canvas_width, height=bg_height)
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))


        # (วาง Labels ทั้งหมด)
        try:
            # ----------------------------------------------------------------------
            # 🟢 START: (แก้ไข) คำนวณ x-position ใหม่ทั้งหมด
            # ----------------------------------------------------------------------
            
            # 1. หาค่า scale ที่ถูกต้อง
            scale = self.current_scale_factor 
            
            # 2. คำนวณความกว้างและจุด x เริ่มต้น (ที่ถูกต้อง)
            final_content_width = int(BILL_CONTENT_WIDTH * scale)
            final_start_x = (canvas_width - final_content_width) // 2
            
            # 3. สร้าง list ของ widgets และ configs
            all_bill_widgets = [
                (self.bill_l1, ORIG_BILL_HEADER_L1),
                (self.bill_l2, ORIG_BILL_HEADER_L2),
                (self.bill_l3, ORIG_BILL_HEADER_L3),
                (self.bill_l4, ORIG_BILL_HEADER_L4),
                (self.bill_d1, ORIG_BILL_DIVIDER1),
                (self.bill_info, ORIG_BILL_INFO_L1),
                (self.bill_d2, ORIG_BILL_DIVIDER2),
                (self.bill_body_h, ORIG_BILL_BODY_HEADER),
                (self.bill_body_i, ORIG_BILL_BODY_ITEM),
                (self.bill_d3, ORIG_BILL_DIVIDER3),
                (self.bill_sub, ORIG_BILL_SUBTOTAL),
                (self.bill_vat, ORIG_BILL_VAT),
                (self.bill_total, ORIG_BILL_TOTAL),
                (self.bill_f1, ORIG_BILL_FOOTER1),
                (self.bill_f2, ORIG_BILL_FOOTER2)
            ]

            # 4. วนลูป place_and_scale โดยใช้ X, W ที่เราคำนวณใหม่
            for widget, orig_config in all_bill_widgets:
                
                # สร้าง config ใหม่ขึ้นมา
                temp_config = {
                    "x": final_start_x / scale, # ⭐️ De-scale X
                    "y": orig_config["y"], # (ใช้ Y, H เดิมจาก config)
                    "width": BILL_CONTENT_WIDTH, # ⭐️ De-scale W
                    "height": orig_config["height"]
                }
                
                self._place_and_scale_widget(widget, temp_config, scale, self.background_label)

            # ----------------------------------------------------------------------
            # 🟢 END: (แก้ไข)
            # ----------------------------------------------------------------------
        except Exception as e:
                 print(f"🔴 ERROR in _on_resize_bill_page (widget place): {e}")

# ----------------------------------------------------------------------
# 🟢 END: (แก้ไขใหม่ทั้งหมด) หน้าบิล (Bill Page)
# ----------------------------------------------------------------------
        else:
            self.current_scale_factor = 1.0 # (ตั้งค่าพื้นฐาน)
            bg_height = self.main_canvas.winfo_height()
            if bg_height < 50: bg_height = 800 # (ตั้งค่า default)
            self.background_label.config(image=None, width=canvas_width, height=bg_height)
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

        

    # ----------------------------------------------------------------------
    # 🟢 START: (แก้ไข 1) ฟังก์ชัน Pop-up จ่ายเงิน
    # ----------------------------------------------------------------------
    def _show_payment_popup(self, person_name, amount):
        """
        🟢 NEW: สร้างหน้าต่าง Pop-up สำหรับแสดง QR Code จ่ายเงิน
        """
        popup = tk.Toplevel(self)
        popup.title(f"ชำระเงินสำหรับ {person_name}")
        popup.geometry("350x450") # ขนาดหน้าต่าง
        popup.configure(bg="#F0F8FF") # สีพื้นหลัง
        popup.resizable(False, False)
        
        # ----------------------------------------------------------------------
        # 🟢 START: (แก้ไข 1) เปลี่ยนชื่อไฟล์เป็น .jpg (ตามคำขอ)
        # ----------------------------------------------------------------------
        qr_image_path = os.path.join(BASE_DIR, "qr.jpg") # 🟢 NEW: (แก้ไข 1) เปลี่ยนเป็น qr.jpg
        # ----------------------------------------------------------------------
        # 🟢 END: (แก้ไข 1)
        # ----------------------------------------------------------------------
        
        try:
            qr_image_open = Image.open(qr_image_path)
            qr_image_resized = qr_image_open.resize((250, 250), Image.Resampling.LANCZOS)
            # ⭐️ ต้องเก็บ reference ของ PhotoImage ไว้
            self.qr_photo_tk = ImageTk.PhotoImage(qr_image_resized) 
            
            qr_label = tk.Label(popup, image=self.qr_photo_tk, bg="#F0F8FF")
            qr_label.pack(pady=20)

        except FileNotFoundError:
            # 🟢 (แก้ไข 1) อัปเดตข้อความ Error ให้ตรง
            print(f"🔴 ERROR: ไม่พบไฟล์ 'qr.jpg' ที่: {qr_image_path}") # 🟢 NEW: (แก้ไข 1) อัปเดตข้อความ Error
            qr_label = tk.Label(popup, 
                                text="ไม่พบไฟล์ 'qr.jpg'!", # 🟢 NEW: (แก้ไข 1) อัปเดตข้อความ Error
                                fg="red", bg="#F0F8FF", font=("Arial", 16, "bold"))
            qr_label.pack(pady=(100, 20)) # จัดให้อยู่กลางๆ
        except Exception as e:
            # 🟢 (แก้ไข 1) อัปเดตข้อความ Error (กรณีไฟล์ .pdf จริง)
            print(f"🔴 ERROR loading {qr_image_path}: {e}")
            error_text = f"เกิดข้อผิดพลาด: {e}\n\n(ไม่สามารถโหลด 'qr.jpg')" # 🟢 NEW: (แก้ไข 1) อัปเดตข้อความ Error
            qr_label = tk.Label(popup, text=error_text, fg="red", bg="#F0F8FF", font=("Arial", 12))
            qr_label.pack(pady=(100, 20))

        # --- แสดงจำนวนเงิน ---
        amount_label = tk.Label(popup, 
                                text=f"จำนวนเงิน: {amount} บาท", 
                                font=("Arial", 18, "bold"), 
                                bg="#F0F8FF")
        amount_label.pack(pady=10)

        # --- ปุ่มยืนยัน ---
        confirm_button = tk.Button(popup, 
                                   text="ยืนยัน", 
                                   font=("Arial", 14), 
                                   width=15,
                                   bg="#4CAF50", fg="white", 
                                   command=lambda: self._on_confirm_payment(popup))
        confirm_button.pack(pady=15)
        
        # --- ทำให้หน้าต่างนี้อยู่บนสุด ---
        popup.grab_set() # บังคับให้ focus
        popup.wait_window() # รอจนกว่าหน้าต่างนี้จะปิด
    # ----------------------------------------------------------------------
    # 🟢 END: (แก้ไข 1)
    # ----------------------------------------------------------------------
       
    # ไปเอามาใส่ตรงนี้
    # ----------------------------------------------------------------------
    # 🟢 START: (เพิ่ม) หน้าบิล (Bill Page)
    # ----------------------------------------------------------------------
    def show_bill_page(self):
        """ 🟢 NEW: (เพิ่ม) แสดงหน้าบิล (หน้าสรุปยอด) """
        self.main_canvas = self._create_canvas_with_scrollbar(self.content_frame)
        frame_bg = "#FFFFFF" # (สีขาว)
        
        # (ตั้งค่าพื้นหลังตามรูป)
        if not self.original_bill_page_image:
            print("🔴 WARNING: ไม่พบ 'หน้าบิล.png', ใช้พื้นหลังสีขาวแทน")
            frame_bg = "#FFFFFF"
            
        self.scrollable_frame_bill = self._setup_scrollable_frame(self.main_canvas, frame_bg)
        
        self.background_label = tk.Label(self.scrollable_frame_bill, image=None, borderwidth=0, bg=frame_bg)
        self.background_label.pack(); 
        self.background_label.bind('<Button-1>', self.get_click_position)
        
        # --- 1. คำนวณค่าต่างๆ (VAT 7% Included) ---
        VAT_RATE = 0.07
        total_amount = self.final_bill_amount
        person_count = self.final_bill_person_count
        
        # (คำนวณ VAT 7% จากราคาเต็ม)
        amount_before_vat = total_amount / (1 + VAT_RATE)
        vat_amount = total_amount - amount_before_vat

        # 🟢 NEW: (เพิ่ม) ตั้งค่าความยาวเส้นคั่น
        self.bill_divider_var.set("-" * 80) 
        
        # --- 2. ตั้งค่า StringVars (🟢 แก้ไข: จัดชิดซ้าย-ขวา) ---
        
        # (Header)
        self.bill_header_l1_var.set("Mooay Noi Shabu")
        self.bill_header_l2_var.set("246 หมู่ 3 ถ.มิตรภาพ ต.ศิลา")
        self.bill_header_l3_var.set("อ.เมือง จ.ขอนแก่น 40000")
        self.bill_header_l4_var.set("โทร. 0XX-XXX-XXXX | เลขประจำตัวผู้เสียภาษี: 0123456789012")
        
        # 🟢 (เพิ่ม) กำหนดความกว้างคอลัมน์
        RECEIPT_LINE_WIDTH = 48 # (ความกว้างรวมโดยประมาณ)
        LEFT_COL_WIDTH = 32     # (ความกว้างคอลัมน์ซ้าย)
        RIGHT_COL_WIDTH = 15    # (ความกว้างคอลัมน์ขวา)

        # (Info - จัดชิดซ้าย)
        table_name = self.current_table_name_var.get() or "N/A"
        current_time = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        self.bill_info_l1_var.set(f"โต๊ะ: {table_name} วันที่: {current_time}".ljust(RECEIPT_LINE_WIDTH)) # 🟢 (จัดชิดซ้าย)
        
        # (Body - จัดซ้าย/ขวา)
        header_l = "รายการ (Description)"
        header_r = "จำนวนเงิน (Amount)"
        self.bill_body_header_var.set(f"{header_l.ljust(LEFT_COL_WIDTH)} {header_r.rjust(RIGHT_COL_WIDTH)}") # 🟢 (จัดฟอร์แมต)

        item_l = f"บุฟเฟ่ต์ชาบู ({person_count} ท่าน)"
        item_r = f"{total_amount:.2f}"
        self.bill_body_item_var.set(f"{item_l.ljust(LEFT_COL_WIDTH)} {item_r.rjust(RIGHT_COL_WIDTH)}") # 🟢 (จัดฟอร์แมต)

        # (Total - จัดซ้าย/ขวา)
        sub_l = "ยอดรวม (Total):"
        sub_r = f"{amount_before_vat:.2f}"
        self.bill_subtotal_var.set(f"{sub_l.ljust(LEFT_COL_WIDTH)} {sub_r.rjust(RIGHT_COL_WIDTH)}") # 🟢 (จัดฟอร์แมต)

        vat_l = "ภาษีมูลค่าเพิ่ม (VAT 7%):"
        vat_r = f"{vat_amount:.2f}"
        self.bill_vat_var.set(f"{vat_l.ljust(LEFT_COL_WIDTH)} {vat_r.rjust(RIGHT_COL_WIDTH)}") # 🟢 (จัดฟอร์แมต)

        total_l = "ยอดสุทธิ (Grand Total):"
        total_r = f"{total_amount:.2f}"
        self.bill_total_var.set(f"{total_l.ljust(LEFT_COL_WIDTH)} {total_r.rjust(RIGHT_COL_WIDTH)}") # 🟢 (จัดฟอร์แมต)

        # (Footer - กลับมาจัดกลาง)
        self.bill_footer1_var.set("(ชำระแล้วโดย QR Code)")
        self.bill_footer2_var.set("ขอบคุณที่มาอุดหนุนนะคะ 💖")

        # --- 3. สร้าง Labels ---
        # (กำหนดค่า Font และ Anchor)
        align_center = "center" # 🟢 (สำหรับ Header/Footer)
        align_receipt = "center"     # 🟢 (สำหรับเนื้อหาบิล - ชิดซ้าย)
        
        header_font = ("Arial", 14, "bold")
        body_font = ("Arial", 11)
        
        # 🟢 (ฟอนต์สำหรับบิล - ต้องเป็น Monospace)
        receipt_font = ("Courier", 11) 
        receipt_font_bold = ("Courier", 11, "bold")
        receipt_total_font = ("Courier", 12, "bold")

        # (สร้าง Widgets)
        # (Header - ใช้ Arial / Center)
        self.bill_l1 = tk.Label(self.background_label, textvariable=self.bill_header_l1_var, font=("Arial", 18, "bold"), bg=frame_bg, anchor=align_center)
        self.bill_l2 = tk.Label(self.background_label, textvariable=self.bill_header_l2_var, font=body_font, bg=frame_bg, anchor=align_center)
        self.bill_l3 = tk.Label(self.background_label, textvariable=self.bill_header_l3_var, font=body_font, bg=frame_bg, anchor=align_center)
        self.bill_l4 = tk.Label(self.background_label, textvariable=self.bill_header_l4_var, font=body_font, bg=frame_bg, anchor=align_center)
        
        # (Receipt Body - ใช้ Courier / Left-aligned)
        self.bill_d1 = tk.Label(self.background_label, textvariable=self.bill_divider_var, font=receipt_font, bg=frame_bg, anchor=align_receipt)
        self.bill_info = tk.Label(self.background_label, textvariable=self.bill_info_l1_var, font=receipt_font, bg=frame_bg, anchor=align_receipt) # 🟢 แก้ไข
        self.bill_d2 = tk.Label(self.background_label, textvariable=self.bill_divider_var, font=receipt_font, bg=frame_bg, anchor=align_receipt)
        
        self.bill_body_h = tk.Label(self.background_label, textvariable=self.bill_body_header_var, font=receipt_font_bold, bg=frame_bg, anchor=align_receipt) # 🟢 แก้ไข
        self.bill_body_i = tk.Label(self.background_label, textvariable=self.bill_body_item_var, font=receipt_font, bg=frame_bg, anchor=align_receipt) # 🟢 แก้ไข
        self.bill_d3 = tk.Label(self.background_label, textvariable=self.bill_divider_var, font=receipt_font, bg=frame_bg, anchor=align_receipt)

        self.bill_sub = tk.Label(self.background_label, textvariable=self.bill_subtotal_var, font=receipt_font, bg=frame_bg, anchor=align_receipt) # 🟢 แก้ไข
        self.bill_vat = tk.Label(self.background_label, textvariable=self.bill_vat_var, font=receipt_font, bg=frame_bg, anchor=align_receipt) # 🟢 แก้ไข
        self.bill_total = tk.Label(self.background_label, textvariable=self.bill_total_var, font=receipt_total_font, bg=frame_bg, anchor=align_receipt) # 🟢 แก้ไข (Font ใหญ่)

        # (Footer - ใช้ Arial / Center)
        self.bill_f1 = tk.Label(self.background_label, textvariable=self.bill_footer1_var, font=body_font, bg=frame_bg, anchor=align_center)
        self.bill_f2 = tk.Label(self.background_label, textvariable=self.bill_footer2_var, font=header_font, bg=frame_bg, anchor=align_center)

        self.main_canvas.bind('<Configure>', self._on_resize_bill_page)
        self.after(100, lambda: self._on_resize_bill_page(None))

    def _on_resize_bill_page(self, event):
        """ 🟢 NEW: (เพิ่ม) Resize สำหรับหน้าบิล """
        bg_image, tk_image_attr = self.original_bill_page_image, 'bill_page_bg_image_tk'
        
        canvas_width = self.main_canvas.winfo_width()
        if canvas_width < 50: return
        
        if bg_image:
            try:
                orig_width, orig_height = bg_image.size
                if orig_width == 0: return
                scale_factor = canvas_width / float(orig_width); self.current_scale_factor = scale_factor
                target_width, target_height = canvas_width, int(orig_height * scale_factor)
                
                resized_img = bg_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
                setattr(self, tk_image_attr, ImageTk.PhotoImage(resized_img))
                self.background_label.config(image=getattr(self, tk_image_attr), width=target_width, height=target_height)
                self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))
            except Exception as e: 
                print(f"🔴 ERROR in _on_resize_bill_page (image load): {e}")
        else:
            self.current_scale_factor = 1.0 # (ตั้งค่าพื้นฐาน)
            bg_height = self.main_canvas.winfo_height()
            if bg_height < 50: bg_height = 800 # (ตั้งค่า default)
            self.background_label.config(image=None, width=canvas_width, height=bg_height)
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

        # (Place Labels ทั้งหมด)
        try:
            scale = self.current_scale_factor 
            self._place_and_scale_widget(self.bill_l1, ORIG_BILL_HEADER_L1, scale, self.background_label)
            self._place_and_scale_widget(self.bill_l2, ORIG_BILL_HEADER_L2, scale, self.background_label)
            self._place_and_scale_widget(self.bill_l3, ORIG_BILL_HEADER_L3, scale, self.background_label)
            self._place_and_scale_widget(self.bill_l4, ORIG_BILL_HEADER_L4, scale, self.background_label)
            self._place_and_scale_widget(self.bill_d1, ORIG_BILL_DIVIDER1, scale, self.background_label)
            self._place_and_scale_widget(self.bill_info, ORIG_BILL_INFO_L1, scale, self.background_label)
            self._place_and_scale_widget(self.bill_d2, ORIG_BILL_DIVIDER2, scale, self.background_label)
            self._place_and_scale_widget(self.bill_body_h, ORIG_BILL_BODY_HEADER, scale, self.background_label)
            self._place_and_scale_widget(self.bill_body_i, ORIG_BILL_BODY_ITEM, scale, self.background_label)
            self._place_and_scale_widget(self.bill_d3, ORIG_BILL_DIVIDER3, scale, self.background_label)
            self._place_and_scale_widget(self.bill_sub, ORIG_BILL_SUBTOTAL, scale, self.background_label)
            self._place_and_scale_widget(self.bill_vat, ORIG_BILL_VAT, scale, self.background_label)
            self._place_and_scale_widget(self.bill_total, ORIG_BILL_TOTAL, scale, self.background_label)
            self._place_and_scale_widget(self.bill_f1, ORIG_BILL_FOOTER1, scale, self.background_label)
            self._place_and_scale_widget(self.bill_f2, ORIG_BILL_FOOTER2, scale, self.background_label)
        except Exception as e:
                 print(f"🔴 ERROR in _on_resize_bill_page (widget place): {e}")
    # ----------------------------------------------------------------------
    # 🟢 END: (เพิ่ม)
    # ----------------------------------------------------------------------


    # ----------------------------------------------------------------------
    # 🟢 START: (แก้ไข 4) หน้าแก้ (เพิ่ม UI Login)
    # ----------------------------------------------------------------------
    def show_fix_page(self):
        self.main_canvas = self._create_canvas_with_scrollbar(self.content_frame)
        frame_bg = "#CCCCCC" # (สีเทา ถ้าไม่มีรูป)
        
        # 🟢 (แก้ไข) ตั้งค่าพื้นหลังตามรูป ถ้ามี
        if self.original_fix_page_image:
            frame_bg = "#FFFFFF" # (หรือสีที่เข้ากับรูป)
            
        self.scrollable_frame_fix = self._setup_scrollable_frame(self.main_canvas, frame_bg)
        
        self.background_label = tk.Label(self.scrollable_frame_fix, image=None, borderwidth=0, bg=frame_bg)
        self.background_label.pack(); 
        self.background_label.bind('<Button-1>', self.get_click_position)

        # 🟢 (ลบ) ลบ placeholder

        # 🟢 (เพิ่ม) สร้าง UI fields (เหมือนหน้า Login)
        self.fix_username_text_label = tk.Label(self.background_label, text="ชื่อผู้ใช้:", font=("Arial", 10, "bold"), anchor="w", bg=frame_bg, fg="#C74136")
        self.fix_password_text_label = tk.Label(self.background_label, text="รหัสผ่าน:", font=("Arial", 10, "bold"), anchor="w", bg=frame_bg, fg="#C74136")
        self.fix_username_entry = tk.Entry(self.background_label, textvariable=self.fix_username_var, font=("Arial", 12), relief="flat", bd=0, bg="white")
        self.fix_password_entry = tk.Entry(self.background_label, textvariable=self.fix_password_var, font=("Arial", 12), show="*", relief="flat", bd=0, bg="white")

        self.main_canvas.bind('<Configure>', self._on_resize_fix_page)
        self.after(100, lambda: self._on_resize_fix_page(None))

    def _on_resize_fix_page(self, event):
        bg_image, tk_image_attr = self.original_fix_page_image, 'fix_page_bg_image_tk'
        
        canvas_width = self.main_canvas.winfo_width()
        if canvas_width < 50: return
        
        if bg_image:
            try:
                orig_width, orig_height = bg_image.size
                if orig_width == 0: return
                scale_factor = canvas_width / float(orig_width); self.current_scale_factor = scale_factor
                target_width, target_height = canvas_width, int(orig_height * scale_factor)
                
                resized_img = bg_image.resize((target_width, target_height), Image.Resampling.LANCZOS)
                setattr(self, tk_image_attr, ImageTk.PhotoImage(resized_img))
                self.background_label.config(image=getattr(self, tk_image_attr), width=target_width, height=target_height)
                self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

                # ----------------------------------------------------------------------
                # 🟢 START: (แก้ไข 4) ขยับกรอบช่องกรอกลง (ใช้พิกัดใหม่)
                # ----------------------------------------------------------------------
                self._place_and_scale_widget(self.fix_username_text_label, ORIG_FIX_USERNAME_LABEL, scale_factor, self.background_label, is_label=True, bold=True)
                self._place_and_scale_widget(self.fix_username_entry, ORIG_FIX_USERNAME_BOX, scale_factor, self.background_label)
                self._place_and_scale_widget(self.fix_password_text_label, ORIG_FIX_PASSWORD_LABEL, scale_factor, self.background_label, is_label=True, bold=True)
                self._place_and_scale_widget(self.fix_password_entry, ORIG_FIX_PASSWORD_BOX, scale_factor, self.background_label)
                # ----------------------------------------------------------------------
                # 🟢 END: (แก้ไข 4)
                # ----------------------------------------------------------------------

            except Exception as e: 
                print(f"🔴 ERROR in _on_resize_fix_page (image load): {e}")
        
        else: # (ถ้าไม่มีรูป)
            self.current_scale_factor = 1.0
            bg_height = self.main_canvas.winfo_height()
            if bg_height < 50: bg_height = 800 # (ตั้งค่า default)
                
            self.background_label.config(image=None, width=canvas_width, height=bg_height)
            self.main_canvas.configure(scrollregion=self.main_canvas.bbox("all"))

            # ----------------------------------------------------------------------
            # 🟢 START: (แก้ไข 4) ขยับกรอบช่องกรอกลง (กรณีไม่มีรูป)
            # ----------------------------------------------------------------------
            x_center = canvas_width // 2
            # (ใช้พิกัด Y ที่ขยับแล้ว จาก ORIG_FIX_...)
            y_label1 = int(ORIG_FIX_USERNAME_LABEL['y'] * self.current_scale_factor)
            y_box1 = int(ORIG_FIX_USERNAME_BOX['y'] * self.current_scale_factor)
            y_label2 = int(ORIG_FIX_PASSWORD_LABEL['y'] * self.current_scale_factor)
            y_box2 = int(ORIG_FIX_PASSWORD_BOX['y'] * self.current_scale_factor)
            
            self.fix_username_text_label.place(x=x_center, y=y_label1, width=300, height=30, anchor="n")
            self.fix_username_entry.place(x=x_center, y=y_box1, width=300, height=40, anchor="n")
            self.fix_password_text_label.place(x=x_center, y=y_label2, width=300, height=30, anchor="n")
            self.fix_password_entry.place(x=x_center, y=y_box2, width=300, height=40, anchor="n")
            # ----------------------------------------------------------------------
            # 🟢 END: (แก้ไข 4)
            # ----------------------------------------------------------------------

        # (ลบ placeholder)
        if hasattr(self, 'fix_placeholder_label'):
            self.fix_placeholder_label.place_forget()
    # ----------------------------------------------------------------------
    # 🟢 END: (แก้ไข 4)
    # ----------------------------------------------------------------------


# --- เรียกใช้งานโปรแกรม (Run the application) ---
if __name__ == "__main__":
    print("🚀 Starting Shabu Shabu App...")
    # 🟢 (แก้ไข) เพิ่ม 'fix_page_bg' ในไฟล์ที่อนุญาตให้หายไปได้
    missing_files = [name for name, path in IMAGE_PATHS.items() if (not os.path.exists(path) and name not in ["money_page_bg", "fix_page_bg", "bill_page_bg"])]
    if missing_files:
        msg = "Cannot start. Missing image files:\n\n" + "\n".join([f"- {name} ({IMAGE_PATHS[name]})" for name in missing_files])
        root = tk.Tk(); root.withdraw()
        messagebox.showerror("Startup Error - Missing Files", msg); print(f"🔴 FATAL: {msg}")
    else:
        app = ShabuApp()
        app.mainloop()
        print("🛑 Shabu Shabu App closed.")