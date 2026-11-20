import os
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.error import BadRequest

BOT_TOKEN = os.environ.get("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("BOT_TOKEN environment variable is required. Add it in Vercel Project Settings.")
WEBHOOK_SECRET = os.environ.get("WEBHOOK_SECRET", "")

GOOGLE_DRIVE_LINK = "https://drive.google.com/drive/folders/1OT0q-0mxRZNTgafyuHJfd7TGlFqQvoQp"
GOOGLE_FORM_LINK = "https://docs.google.com/forms/d/e/1FAIpQLSciV5HEHKgOIQ_O1nxj836ThG3i807eM5htfp5jdKK7CYrVdQ/viewform?usp=dialog"
CENTRAL_INDUCTION_SCHEDULE_DOC = "https://docs.google.com/document/d/1KmHmllcaUn75UAHYAxsPp3UNKPxEyQ9_/edit?usp=sharing&ouid=113177545693365075177&rtpof=true&sd=true"
INAUGURAL_PROGRAM_DOC = "https://docs.google.com/document/d/1XQOtiJoNa3luDZWqwIMhTDgydX4zm3cx/edit?usp=drivesdk&ouid=104153490061474917624&rtpof=true&sd=true"


def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("🏢 About Company (SAIL)", callback_data="cat_company")],
        [InlineKeyboardButton("💰 Pay and Allowance", callback_data="cat_pay")],
        [InlineKeyboardButton("📜 Leave Rules & Regulations", callback_data="cat_leave")],
        [InlineKeyboardButton("🏥 Medical Benefits", callback_data="cat_medical")],
        [InlineKeyboardButton("📚 Library & Recreation", callback_data="cat_lib")],
        [InlineKeyboardButton("📂 Downloadable Forms & Documents", callback_data="cat_forms")],
        [InlineKeyboardButton("🎓 Central Induction & Schedule", callback_data="cat_induction")],
        [InlineKeyboardButton("📞 Contact Details & Key Numbers", callback_data="cat_contact")],
        [InlineKeyboardButton("💬 Submit Feedback / Queries (Google Form)", url=GOOGLE_FORM_LINK)]
    ]
    return InlineKeyboardMarkup(keyboard)


def get_category_view(cat_id):
    if cat_id == "cat_company":
        text = "🏢 <b>About Company (SAIL)</b>\n\nSelect an official plant portal to visit:"
        keyboard = [
            [InlineKeyboardButton("🌐 SAIL Main Official Portal", url="https://www.sail.co.in")],
            [InlineKeyboardButton("🏬 Bhilai Steel Plant (BSP)", url="https://www.sail.co.in/en/plants/about-bhilai-steel-plant")],
            [InlineKeyboardButton("🏬 Bokaro Steel Plant (BSL)", url="https://www.sail.co.in/en/plants/about-bokaro-steel-plant")],
            [InlineKeyboardButton("🏬 Durgapur Steel Plant (DSP)", url="https://www.sail.co.in/en/plants/about-durgapur-steel-plant")],
            [InlineKeyboardButton("🏬 Rourkela Steel Plant (RSP)", url="https://www.sail.co.in/en/plants/about-rourkela-steel-plant")],
            [InlineKeyboardButton("🏬 IISCO Steel Plant (ISP)", url="https://www.sail.co.in/en/plants/about-iisco-steel-plant")],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
    elif cat_id == "cat_pay":
        text = "💰 <b>Pay and Allowances</b>\n\nSelect an option below to view specific entitlement details or access the full PDF:"
        keyboard = [
            [InlineKeyboardButton("📊 Executive Pay Scales & Allowances", callback_data="detail_pay_scales")],
            [InlineKeyboardButton("✈️ Travelling & Lodging Entitlements", callback_data="detail_pay_ta")],
            [InlineKeyboardButton("📱 Mobile, Furniture & Briefcase Allowances", callback_data="detail_pay_allowances")],
            [InlineKeyboardButton("📄 Full Ready Reckoner PDF (Google Drive)", url=GOOGLE_DRIVE_LINK)],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
    elif cat_id == "cat_leave":
        text = "📜 <b>Leave Rules &amp; Regulations</b>\n\nSelect a leave category to view specific guidelines and eligibility:"
        keyboard = [
            [InlineKeyboardButton("1️⃣ Earned Leave (EL)", callback_data="detail_el_rules")],
            [InlineKeyboardButton("2️⃣ Half Pay (HPL) & Commuted Leave", callback_data="detail_hpl_rules")],
            [InlineKeyboardButton("3️⃣ Maternity & Child Care Leave (CCL)", callback_data="detail_ccl_rules")],
            [InlineKeyboardButton("4️⃣ Special Casual Leave", callback_data="detail_scl_rules")],
            [InlineKeyboardButton("5️⃣ Extraordinary Leave & Leave Not Due", callback_data="detail_eol_rules")],
            [InlineKeyboardButton("6️⃣ Study Leave & Sabbatical Leave", callback_data="detail_study_sabbatical")],
            [InlineKeyboardButton("7️⃣ Important General Rules", callback_data="detail_general_rules")],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
    elif cat_id == "cat_medical":
        text = "🏥 <b>Medical Benefits</b>\n\nChoose an option below to view medical details or download the board form:"
        keyboard = [
            [InlineKeyboardButton("ℹ️ Medical Facilities Overview", callback_data="detail_med_facilities")],
            [InlineKeyboardButton("📋 Executive Medical Examination Board Form", callback_data="detail_med_form_info")],
            [InlineKeyboardButton("📄 Download Medical Form PDF (Google Drive)", url=GOOGLE_DRIVE_LINK)],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
    elif cat_id == "cat_lib":
        text = "📚 <b>Library and Recreation Facilities</b>\n\nSelect a topic to view details:"
        keyboard = [
            [InlineKeyboardButton("📖 Central & Public Library Rules", callback_data="detail_lib_info")],
            [InlineKeyboardButton("⚽ Sports & Recreation Facilities", callback_data="detail_sports_info")],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
    elif cat_id == "cat_forms":
        text = "📂 <b>Downloadable Forms &amp; Documents</b>\n\nAll official documents, medical forms, and ready reckoners are hosted in our public Google Drive folder."
        keyboard = [
            [InlineKeyboardButton("📄 Open Google Drive Forms Folder", url=GOOGLE_DRIVE_LINK)],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
    elif cat_id == "cat_induction":
        text = "🎓 <b>Central Induction &amp; Schedule</b>\n\nInformation regarding inaugural programs, plant orientation, dress codes, and video links:"
        keyboard = [
            [InlineKeyboardButton("🏛️ Inaugural Program & Schedule", url=INAUGURAL_PROGRAM_DOC)],
            [InlineKeyboardButton("📄 Central Induction Schedule Document", url=CENTRAL_INDUCTION_SCHEDULE_DOC)],
            [InlineKeyboardButton("👔 Suggested Dress Code", callback_data="detail_ind_dresscode")],
            [InlineKeyboardButton("🎥 Informative Video Links (Google Drive)", url=GOOGLE_DRIVE_LINK)],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
    elif cat_id == "cat_contact":
        text = "📞 <b>Contact Details &amp; Key Numbers</b>\n\nAccess direct contacts for HR-L&amp;D officials and hostel administration:"
        keyboard = [
            [InlineKeyboardButton("☎️ HR-L&D Officials & Hostel Warden Directory", callback_data="detail_contacts_list")],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
    else:
        text = "Welcome to SAIL-BSP Information Assistant!"
        keyboard = [[InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]]

    return text, InlineKeyboardMarkup(keyboard)


def get_detail_view(detail_id):
    parent_cat = "main_menu"

    if detail_id == "detail_pay_scales":
        parent_cat = "cat_pay"
        text = (
            "📊 <b>BSP Executive Pay Scales (w.e.f. 01/01/2017)</b>\n\n"
            "• <b>E0:</b> ₹30,000 – 3% – ₹1,20,000\n"
            "• <b>E1 (MTs):</b> ₹50,000 – ₹1,60,000 (Placed in ₹60,000 – ₹1,80,000 after 1 yr/training)\n"
            "• <b>E2:</b> ₹70,000 – ₹2,00,000 | <b>E3:</b> ₹80,000 – ₹2,20,000\n"
            "• <b>E4:</b> ₹90,000 – ₹2,40,000 | <b>E5:</b> ₹1,00,000 – ₹2,60,000\n"
            "• <b>E6:</b> ₹1,20,000 – ₹2,80,000 | <b>E7/E8:</b> ₹1,20,000 – ₹2,80,000\n"
            "• <b>E9:</b> ₹1,50,000 – ₹3,00,000 | <b>Director/CEO:</b> ₹1,80,000 – ₹3,40,000\n\n"
            "🏥 <i>Non-Practicing Allowance for Doctors:</i> MBBS (16%), Diploma (18%), PG (20%)"
        )
    elif detail_id == "detail_pay_ta":
        parent_cat = "cat_pay"
        text = (
            "✈️ <b>Travelling &amp; Lodging Entitlements</b>\n\n"
            "• <b>E0 – E3:</b> Travel 2AC/CC | Lodging: 3-Star / Actuals up to ₹2,500 | DA: ₹600 (Own: ₹900)\n"
            "• <b>E4 – E6:</b> Travel 1AC/CC or Air Economy | Lodging: 4-Star / Actuals up to ₹3,500 | DA: ₹750 (Own: ₹1,100)\n"
            "• <b>E7 – E8:</b> Travel 1AC/CC or Air Economy | Lodging: 4-Star / Actuals up to ₹4,500 | DA: ₹900 (Own: ₹1,300)\n"
            "• <b>E9 / Directors:</b> Air Executive / Premium Economy | Lodging: Actuals | DA: ₹1,000 – ₹1,100"
        )
    elif detail_id == "detail_pay_allowances":
        parent_cat = "cat_pay"
        text = (
            "📱 <b>Mobile, Furniture &amp; Briefcase Allowances</b>\n\n"
            "• <b>Mobile Hardware Purchase (Once in 3 Yrs):</b>\n"
            "  - E0–E4: ₹10,000 | E5–E6: ₹15,000 | E7: ₹19,000 | E8: ₹25,000 | E9: ₹30,000\n"
            "• <b>Monthly Mobile Reimbursement:</b> E0 (₹200) to E8 (₹1,100) / E9 (Actuals)\n"
            "• <b>Furniture Allowance:</b> E1 (₹15,000), E2–E3 (₹25,000), E4–E5 (₹50,000), E6 (₹1,00,000), E7 (₹1,50,000), E8 (₹2,50,000), E9 (₹4,00,000)\n"
            "• <b>Briefcase Allowance (Once in 4 Yrs):</b> E0–E3 (₹2,150), E4–E6 (₹2,300), E7+ (₹2,600)"
        )
    elif detail_id == "detail_el_rules":
        parent_cat = "cat_leave"
        text = (
            "📋 <b>Earned Leave (EL) Rules</b>\n\n"
            "• <b>Credit:</b> Earned at 1 day for every 11 days of service.\n"
            "• <b>Accumulation Limit:</b> Maximum accumulation allowed is 300 days.\n"
            "• <b>Encashment:</b> Permitted as per company guidelines during service/retirement."
        )
    elif detail_id == "detail_hpl_rules":
        parent_cat = "cat_leave"
        text = (
            "📋 <b>Half Pay Leave (HPL) &amp; Commuted Leave</b>\n\n"
            "• <b>Credit:</b> 20 days for each completed year of service.\n"
            "• <b>Commuted Leave:</b> Granted on medical grounds against twice the amount of HPL."
        )
    elif detail_id == "detail_ccl_rules":
        parent_cat = "cat_leave"
        text = (
            "📋 <b>Maternity &amp; Child Care Leave (CCL)</b>\n\n"
            "• <b>Maternity Leave:</b> Up to 180 days for female employees.\n"
            "• <b>Child Care Leave (CCL):</b> Available for raising children up to 18 years of age."
        )
    elif detail_id == "detail_scl_rules":
        parent_cat = "cat_leave"
        text = (
            "📋 <b>Special Casual Leave</b>\n\n"
            "• Granted for family planning, sports events, union activities, and voluntary blood donation."
        )
    elif detail_id == "detail_eol_rules":
        parent_cat = "cat_leave"
        text = (
            "📋 <b>Extraordinary Leave &amp; Leave Not Due</b>\n\n"
            "• <b>Extraordinary Leave (EOL):</b> Granted when no other leave is admissible.\n"
            "• <b>Leave Not Due:</b> Advanced leave granted on medical certificate."
        )
    elif detail_id == "detail_study_sabbatical":
        parent_cat = "cat_leave"
        text = (
            "📋 <b>Study Leave &amp; Sabbatical Leave</b>\n\n"
            "• <b>Study Leave:</b> Granted for pursuing higher technical or management qualifications.\n"
            "• <b>Sabbatical:</b> Permitted for approved professional development or personal growth."
        )
    elif detail_id == "detail_general_rules":
        parent_cat = "cat_leave"
        text = (
            "📋 <b>Important General Leave Rules</b>\n\n"
            "• Leave cannot be claimed as a matter of right.\n"
            "• Prior approval from sanctioning authority is required before proceeding on leave."
        )
    elif detail_id == "detail_med_facilities":
        parent_cat = "cat_medical"
        text = (
            "🏥 <b>Medical Facilities Overview</b>\n\n"
            "• <b>Hostel Hospital:</b> Dispensary near Sector-1 Hostel.\n"
            "• <b>Main Hospital:</b> Jawaharlal Nehru Hospital &amp; Research Centre in Hospital Sector (860 beds).\n"
            "• <b>Access:</b> Avail medical services using the Medical Card issued during training."
        )
    elif detail_id == "detail_med_form_info":
        parent_cat = "cat_medical"
        text = (
            "📋 <b>Executive Medical Examination Board Form</b>\n\n"
            "• Required prior to appointment for Executive posts under SAIL.\n"
            "• Includes Candidate's Declaration (medical history, family history) and Medical Board Physical Examination report (vision, chest, vitals).\n"
            "• <b>Note:</b> Download the full printable form from the Google Drive link below."
        )
    elif detail_id == "detail_lib_info":
        parent_cat = "cat_lib"
        text = (
            "📖 <b>Library Facilities</b>\n\n"
            "• <b>Central Library (HRDC):</b> Open 09:00 AM to 05:30 PM. Borrow 2 books for 30 days.\n"
            "• <b>Public Library:</b> New Civic Centre (Annual membership applies)."
        )
    elif detail_id == "detail_sports_info":
        parent_cat = "cat_lib"
        text = (
            "⚽ <b>Sports &amp; Recreation</b>\n\n"
            "• Indoor/outdoor games and Gym available at the Hostel.\n"
            "• Multiple stadia and playgrounds located near the Hostel."
        )
    elif detail_id == "detail_ind_dresscode":
        parent_cat = "cat_induction"
        text = (
            "👔 <b>Suggested Dress Code During Central Induction Programme</b>\n\n"
            "To ensure uniformity and comfort during various induction activities, trainees are advised to follow the dress code given below:\n\n"
            "1️⃣ <b>Medical Examination</b>\n"
            "• <b>Boys:</b> Half-sleeve T-shirt, Lower/track pants, Comfortable sports shoes\n"
            "• <b>Girls:</b> Half-sleeve T-shirt with lower/track pants OR Loose-fitting Salwar-Kurta, Comfortable sports shoes or sandals\n\n"
            "2️⃣ <b>Document Verification</b>\n"
            "• Casual, decent, light-coloured attire is recommended.\n"
            "• <i>Examples:</i> T-shirt/Shirt with trousers/jeans, Comfortable shoes or sandals\n\n"
            "3️⃣ <b>Central Induction Programme &amp; Classroom Sessions</b>\n"
            "• <b>Boys:</b> Plain, light-coloured formal shirt, Dark-coloured formal trousers, Formal shoes\n"
            "• <b>Girls:</b> Plain, light-coloured formal attire (Formal shirt &amp; trousers / Salwar Suit / Saree), Formal footwear\n\n"
            "4️⃣ <b>Footwear Guidelines</b>\n"
            "All trainees are advised to bring:\n"
            "• One pair of sports shoes (for medical examination and other activities)\n"
            "• One pair of formal shoes (for induction sessions and classroom training)"
        )
    elif detail_id == "detail_contacts_list":
        parent_cat = "cat_contact"
        text = (
            "📞 <b>Useful Telephone Numbers &amp; Official Contacts</b>\n\n"
            "• <i>STD Code for Bhilai:</i> 0788\n"
            "• <i>Note:</i> For dialing auto exchange numbers from outside Bhilai or P&amp;T, dial 0788-28xxxxx\n\n"
            "1️⃣ <b>Sanjeev Shrivastava</b>\n"
            "• <b>Designation:</b> GM I/c (HR-L and D)\n"
            "• <b>Office Ext:</b> 54900 | <b>Mobile:</b> 9407982131\n"
            "• <b>E-mail:</b> skshrivastava@sail.in\n\n"
            "2️⃣ <b>Yashvant Singh Jowhari</b>\n"
            "• <b>Designation:</b> DGM (HR-L and D)\n"
            "• <b>Office Ext:</b> 54925 | <b>Mobile:</b> 9407981115\n"
            "• <b>E-mail:</b> ysjowhari@sail.in\n\n"
            "3️⃣ <b>Neeraja Sharma</b>\n"
            "• <b>Designation:</b> DGM (HR-L and D)\n"
            "• <b>Office Ext:</b> 54913 | <b>Mobile:</b> 9407981854\n"
            "• <b>E-mail:</b> Neeraja.sharma@sail.in\n\n"
            "4️⃣ <b>Sushmita Patla</b>\n"
            "• <b>Designation:</b> Dy.Mgr (HR-L and D)\n"
            "• <b>Office Ext:</b> 54904 | <b>Mobile:</b> 9407982137\n"
            "• <b>E-mail:</b> sushmitapatla@sail.in\n\n"
            "5️⃣ <b>Sanjay Singh</b>\n"
            "• <b>Designation:</b> Hostel Warden\n"
            "• <b>Office Ext:</b> 58973 | <b>Mobile:</b> 9479277645\n"
            "• <b>E-mail:</b> Sanjaysingh1025@gmail.com"
        )

    keyboard = [
        [InlineKeyboardButton("◀️ Back to Category Menu", callback_data=parent_cat)],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
    ]
    return text, InlineKeyboardMarkup(keyboard)


ptb_app = Application.builder().token(BOT_TOKEN).updater(None).build()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "ℹ️ <b>Welcome to SAIL-BSP Information Assistant!</b>\n\n"
        "Please choose a category below to view information:",
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard()
    )


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    try:
        if data == "main_menu":
            await query.edit_message_text(
                "ℹ️ <b>Welcome to SAIL-BSP Information Assistant!</b>\n\n"
                "Please choose a category below to view information:",
                parse_mode="HTML",
                reply_markup=get_main_menu_keyboard()
            )
        elif data.startswith("cat_"):
            text, markup = get_category_view(data)
            await query.edit_message_text(text, parse_mode="HTML", reply_markup=markup)
        elif data.startswith("detail_"):
            text, markup = get_detail_view(data)
            await query.edit_message_text(text, parse_mode="HTML", reply_markup=markup)
    except BadRequest:
        pass


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Thank you for your message! Please send /start or use the menu buttons to navigate.")


ptb_app.add_handler(CommandHandler("start", start))
ptb_app.add_handler(CallbackQueryHandler(button_click))
ptb_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))


@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Initialize the Telegram application once per warm Vercel Function instance.
    await ptb_app.initialize()
    await ptb_app.start()
    try:
        yield
    finally:
        await ptb_app.stop()
        await ptb_app.shutdown()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def health():
    return {"status": "ok"}


@app.post("/webhook")
async def telegram_webhook(request: Request):
    if WEBHOOK_SECRET:
        header_secret = request.headers.get("X-Telegram-Bot-Api-Secret-Token", "")
        if header_secret != WEBHOOK_SECRET:
            return Response(status_code=403)
    data = await request.json()
    update = Update.de_json(data, ptb_app.bot)
    # The application is initialized by FastAPI's lifespan handler.
    await ptb_app.process_update(update)
    return Response(status_code=200)
