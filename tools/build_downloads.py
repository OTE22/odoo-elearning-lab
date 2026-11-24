"""Build the downloadable Excel job aids served by nova_learning_studio.

Each workbook is right-to-left, starts with an instructions sheet, uses live
formulas and drop-down lists, and is pre-filled with the course's own case so
learners can see a correct example before replacing it with their data.

    python tools/build_downloads.py      (requires openpyxl)
"""
from pathlib import Path

from openpyxl import Workbook
from openpyxl.formatting.rule import FormulaRule
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.worksheet.datavalidation import DataValidation

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "addons/nova_learning_studio/static/downloads"
COLORS = {"proposal_writing": "753953", "ai_cultural_work": "324B77", "digital_safety": "155852"}
THIN = Side(style="thin", color="D6DFE0")
BOX = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)
FONT = "Tahoma"


def sheet(wb, title, color, headers, widths, rows=(), first=False):
    ws = wb.active if first else wb.create_sheet()
    ws.title = title
    ws.sheet_view.rightToLeft = True
    head = PatternFill("solid", fgColor=color)
    for col, (text, width) in enumerate(zip(headers, widths), start=1):
        cell = ws.cell(row=1, column=col, value=text)
        cell.font = Font(name=FONT, bold=True, color="FFFFFF")
        cell.fill = head
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        cell.border = BOX
        ws.column_dimensions[cell.column_letter].width = width
    ws.row_dimensions[1].height = 32
    for r, row in enumerate(rows, start=2):
        for c, value in enumerate(row, start=1):
            cell = ws.cell(row=r, column=c, value=value)
            cell.font = Font(name=FONT)
            cell.alignment = Alignment(vertical="top", wrap_text=True, horizontal="right")
            cell.border = BOX
    ws.freeze_panes = "A2"
    return ws


def intro(wb, color, title, lines):
    ws = wb.active
    ws.title = "تعليمات"
    ws.sheet_view.rightToLeft = True
    ws.column_dimensions["A"].width = 100
    ws["A1"] = title
    ws["A1"].font = Font(name=FONT, size=16, bold=True, color=color)
    for i, line in enumerate(lines, start=3):
        ws.cell(row=i, column=1, value=line).font = Font(name=FONT, size=11)
        ws.cell(row=i, column=1).alignment = Alignment(wrap_text=True, horizontal="right")
    ws.cell(row=len(lines) + 4, column=1, value="أكاديمية NovaTechAI · learn.novatechai.site — الأمثلة افتراضية لأغراض التدريب.").font = \
        Font(name=FONT, size=9, italic=True, color="5B6B73")


def money(ws, cols, rows):
    for col in cols:
        for r in range(2, rows + 2):
            ws[f"{col}{r}"].number_format = "#,##0"


def choices(ws, ref, options):
    dv = DataValidation(type="list", formula1='"' + ",".join(options) + '"', allow_blank=True)
    ws.add_data_validation(dv)
    dv.add(ref)


def flag(ws, ref, formula, color="FDE2E2"):
    ws.conditional_formatting.add(ref, FormulaRule(formula=[formula], fill=PatternFill("solid", fgColor=color)))


def total_row(ws, row, label_col, label, sums):
    ws[f"{label_col}{row}"] = label
    ws[f"{label_col}{row}"].font = Font(name=FONT, bold=True)
    for col, formula in sums.items():
        ws[f"{col}{row}"] = formula
        ws[f"{col}{row}"].font = Font(name=FONT, bold=True)
        ws[f"{col}{row}"].number_format = "#,##0"


# ---------------------------------------------------------------- proposal
def funding_plan(path, color):
    wb = Workbook()
    intro(wb, color, "خطة التمويل والتدفق النقدي", [
        "١. في ورقة «مصادر التمويل» سجّل كل مصدر: نقدي أم عيني، ومؤكد أم وعد، ودليله وموعده.",
        "٢. أدخل الكلفة الكلية ونسبة سقف المنحة؛ تحسب الورقة السقف وتنبّه إن تجاوزه المبلغ المطلوب.",
        "٣. في ورقة «التدفق النقدي» أدخل الداخل والخارج شهرياً؛ يتلوّن الرصيد التراكمي بالأحمر عند العجز.",
        "٤. في «سجل المخاطر» سجّل لكل خطر مؤشراً مبكراً ومسؤولاً وردّاً جاهزاً.",
        "تذكير: المساهمة العينية تُحتسب في الكلفة الكلية لكنها لا تسدّد فاتورة.",
    ])
    ws = sheet(wb, "مصادر التمويل", color,
               ["المصدر", "النوع", "المبلغ", "الحالة", "الدليل", "الموعد"], [26, 12, 14, 14, 34, 16], [
                   ["المنحة الرئيسة", "نقدي", 3000, "مؤكد", "خطاب منح (باليورو)", "عند التوقيع"],
                   ["البلدية: القاعة", "عيني", 800, "مؤكد", "خطاب يحدد القيمة السوقية", "قبل الإرسال"],
                   ["راعٍ محلي", "نقدي", 700, "وعد", "بانتظار التوقيع", "قبل الإرسال بأسبوع"],
                   ["التذاكر", "نقدي", 500, "تقدير", "مبيعات العرض السابق", "بعد العرض"],
               ])
    choices(ws, "B2:B30", ["نقدي", "عيني"])
    choices(ws, "D2:D30", ["مؤكد", "وعد", "تقدير"])
    money(ws, "C", 30)
    labels = [("H2", "الكلفة الكلية", 5000), ("H3", "نسبة سقف المنحة", 0.6),
              ("H4", "سقف المنحة المسموح", "=I2*I3"), ("H5", "المنحة المطلوبة", '=SUMIFS(C:C,A:A,"المنحة الرئيسة")'),
              ("H6", "فحص السقف", '=IF(I5>I4,"يتجاوز السقف","ضمن السقف")'),
              ("H7", "الحاجة النقدية", '=I2-SUMIFS(C:C,B:B,"عيني")'),
              ("H8", "النقد المؤكد", '=SUMIFS(C:C,B:B,"نقدي",D:D,"مؤكد")'),
              ("H9", "النقد غير المؤكد", '=SUMIFS(C:C,B:B,"نقدي")-I8'),
              ("H10", "انخفاض الصرف المفترض", 0.1),
              ("H11", "أسوأ احتمال للنقد", '=I8*(1-I10)+SUMIFS(C:C,A:A,"التذاكر")/2'),
              ("H12", "الفجوة في أسوأ احتمال", "=I7-I11")]
    ws.column_dimensions["H"].width = 26
    ws.column_dimensions["I"].width = 16
    for ref, label, value in labels:
        row = ref[1:]
        ws[ref] = label
        ws[ref].font = Font(name=FONT, bold=True)
        ws[f"I{row}"] = value
        ws[f"I{row}"].number_format = "0%" if row in ("3", "10") else "#,##0"
        ws[f"I{row}"].border = BOX
    flag(ws, "I6", 'I6="يتجاوز السقف"')
    flag(ws, "I12", "I12>0")

    cf = sheet(wb, "التدفق النقدي", color, ["الشهر", "الداخل", "الخارج", "الرصيد التراكمي", "ملاحظة"], [14, 14, 14, 18, 40], [
        ["الشهر ١", 1820, 900, None, "الدفعة الأولى ٧٠٪ من ٢٦٠٠"],
        ["الشهر ٢", 0, 700, None, "جلسات وقاعة"],
        ["الشهر ٣", 0, 500, None, "مواد ونقل"],
        ["الشهر ٤", 780, 500, None, "الدفعة الأخيرة بعد التقرير"],
    ])
    for r in range(2, 14):
        cf[f"D{r}"] = f"=SUM($B$2:B{r})-SUM($C$2:C{r})"
    money(cf, "BCD", 12)
    flag(cf, "D2:D13", "D2<0")

    sheet(wb, "سجل المخاطر", color,
          ["الخطر", "الاحتمال", "الأثر", "المؤشر المبكر", "المسؤول", "الرد الجاهز"], [26, 12, 12, 30, 16, 40], [
              ["انخفاض سعر صرف اليورو", "متوسط", "مرتفع", "تراجع ٥٪ قبل الدفعة الأولى", "المدير المالي", "بند احتياطي إن أجازته الدعوة، أو تقليص مخطط مسبقاً"],
              ["انسحاب الراعي", "متوسط", "مرتفع", "عدم التوقيع قبل الإرسال بأسبوع", "المنسقة", "النسخة الأساسية من المشروع وإبلاغ المانح"],
              ["ضعف مبيعات التذاكر", "مرتفع", "متوسط", "بيع أقل من ٣٠٪ قبل العرض بأسبوعين", "مسؤول الجمهور", "حملة شراكات وتأجيل نفقات غير أساسية"],
          ])
    for name in ("سجل المخاطر",):
        choices(wb[name], "B2:C30", ["منخفض", "متوسط", "مرتفع"])
    wb.save(path)


def indicator_card(path, color):
    wb = Workbook()
    intro(wb, color, "بطاقة المؤشر وسجل القياس", [
        "١. عرّف المؤشر في ورقة «بطاقة المؤشر» قبل جمع أي بيانات.",
        "٢. سجّل في «سجل القياس» كل مشارك برمز داخلي، لا باسمه.",
        "٣. تحسب الورقة البسط والمقام والنسبة، وتُظهر عدد من تعذّر قياسهم إلى جانب النتيجة.",
    ])
    ws = sheet(wb, "بطاقة المؤشر", color, ["البند", "القيمة"], [28, 70], [
        ["اسم المؤشر", "وضوح التحوّل الدرامي في المشهد"],
        ["التعريف", "تحسّن درجة واحدة على الأقل بين القياس القبلي والبعدي على بطاقة من صفر إلى درجتين"],
        ["البسط", "عدد من تحسّنوا درجة واحدة على الأقل"],
        ["المقام", "من لديهم قياسان (قبلي وبعدي)"],
        ["وقت الرصد", "بعد الجلسة الأولى وبعد الجلسة الأخيرة"],
        ["المسؤول", "المنسقة مع ملاحظ ثانٍ مستقل"],
        ["حدود التفسير", "لا يعزل القياس أثر التدريب عن عوامل أخرى؛ يُذكر المفقودون دائماً"],
    ])
    log = sheet(wb, "سجل القياس", color, ["رمز المشارك", "القياس القبلي (٠-٢)", "القياس البعدي (٠-٢)", "لديه قياسان؟", "تحسّن؟"],
                [16, 18, 18, 14, 12],
                [[f"P{n:02}", pre, post] for n, (pre, post) in enumerate(
                    [(0, 1), (1, 2), (0, 2), (1, 1), (0, 1), (1, 2), (0, 0), (1, 2), (0, 1), (2, 2), (0, 1), (1, 2),
                     (0, 1), (1, 1), (0, 1), (1, 2), (0, None), (1, None), (None, None), (None, None)], start=1)])
    for r in range(2, 42):
        log[f"D{r}"] = f'=IF(AND(ISNUMBER(B{r}),ISNUMBER(C{r})),"نعم",IF(A{r}="","","لا"))'
        log[f"E{r}"] = f'=IF(D{r}="نعم",IF(C{r}>B{r},"نعم","لا"),"")'
    choices(log, "B2:C41", ["0", "1", "2"])
    for ref, label, formula in [("G2", "المسجّلون", '=COUNTA(A2:A41)'), ("G3", "لديهم قياسان (المقام)", '=COUNTIF(D2:D41,"نعم")'),
                                ("G4", "تحسّنوا (البسط)", '=COUNTIF(E2:E41,"نعم")'), ("G5", "النسبة", "=IF(H3=0,0,H4/H3)"),
                                ("G6", "تعذّر قياسهم", "=H2-H3")]:
        log[ref] = label
        log[ref].font = Font(name=FONT, bold=True)
        log[f"H{ref[1:]}"] = formula
        log[f"H{ref[1:]}"].border = BOX
    log["H5"].number_format = "0%"
    log.column_dimensions["G"].width = 22
    wb.save(path)


# ---------------------------------------------------------------- AI editing
def claim_log(path, color):
    wb = Workbook()
    intro(wb, color, "سجل التحقق من الادعاءات", [
        "١. قسّم كل جملة في المسودة إلى ادعاءات مستقلة: العدد، والوسيط، والمنشأ، والتاريخ…",
        "٢. اربط كل ادعاء بوثيقة محددة، أو اتركه «معلّقاً» وأحِله إلى صاحب الصلاحية.",
        "٣. لا يُنشر ادعاء حالته «معلّق»؛ يتلوّن الصف بالأحمر للتنبيه.",
        "٤. عند التصحيح بعد النشر، سجّل ما تغيّر ومتى في عمود الملاحظات وانشره في سجل التصحيح.",
    ])
    ws = sheet(wb, "سجل الادعاءات", color,
               ["الجملة في المسودة", "الادعاء", "النوع", "الوثيقة", "الحالة", "القرار التحريري", "المراجِع", "التاريخ", "ملاحظات"],
               [34, 22, 12, 18, 12, 34, 14, 12, 30], [
                   ["١٨ لوحة زيتية من بيروت", "عدد الأعمال ١٨", "عدد", "الوثيقة أ", "مثبت", "يبقى", "المحررة", None, ""],
                   ["١٨ لوحة زيتية من بيروت", "الوسيط: زيت", "وسيط", "الوثيقة أ", "مصحّح", "طبعات على ورق، في اللغتين", "المحررة", None, "صُحح قبل النشر"],
                   ["١٨ لوحة زيتية من بيروت", "المنشأ: بيروت", "منشأ", "—", "معلّق", "تُحذف المدينة ويُحال السؤال إلى القيّمة", "المحررة", None, ""],
                   ["أول معرض في المدينة", "أسبقية المعرض", "أسبقية", "—", "محذوف", "لا دليل؛ يُحذف الادعاء", "المحررة", None, ""],
               ])
    choices(ws, "C2:C200", ["عدد", "تاريخ", "وسيط", "منشأ", "اسم", "اقتباس", "أسبقية", "أخرى"])
    choices(ws, "E2:E200", ["مثبت", "معلّق", "مصحّح", "محذوف"])
    flag(ws, "A2:I200", '$E2="معلّق"')
    for r in range(2, 201):
        ws[f"H{r}"].number_format = "yyyy-mm-dd"
    wb.save(path)


def disclosure_matrix(path, color):
    wb = Workbook()
    intro(wb, color, "مصفوفة قرار الإفصاح عن الذكاء الاصطناعي", [
        "تساعدك المصفوفة على طرح أسئلة المادة ٥٠ من قانون الذكاء الاصطناعي الأوروبي (نافذة منذ ٢ آب/أغسطس ٢٠٢٦).",
        "أجب بنعم أو لا عن كل سؤال؛ يقترح عمود «القرار المقترح» الإفصاح المطلوب، ويبقى القرار النهائي للمسؤول التحريري.",
        "الأداة للتدريب ولا تغني عن استشارة قانونية؛ والقوانين المحلية قد تفرض واجبات أخرى.",
        "تذكير: الاستثناء الخاص بالنص يتطلب شرطين معاً: مراجعة بشرية أو ضبطاً تحريرياً، ومسؤولاً تحريرياً عن النشر.",
    ])
    headers = ["المحتوى", "النوع", "يشبه شخصاً أو حدثاً حقيقياً ويبدو أصيلاً؟", "جزء من عمل فني أو إبداعي واضح؟",
               "نص لإعلام الجمهور بمصلحة عامة؟", "راجعه إنسان أو خضع لضبط تحريري؟", "يوجد مسؤول تحريري عن النشر؟",
               "القرار المقترح", "صيغة الوسم بالعربية", "صيغة الوسم بالإنجليزية", "المعتمِد"]
    ws = sheet(wb, "المصفوفة", color, headers, [26, 10, 18, 18, 18, 18, 18, 40, 30, 28, 14], [
        ["خبر افتتاح المعرض", "نص", "لا", "لا", "نعم", "نعم", "نعم", None, "أُعدّ بمساعدة أداة ذكاء اصطناعي وراجعته هيئة التحرير (اختياري)", "Prepared with AI assistance and reviewed by our editors (optional)", "رئيسة التحرير"],
        ["ملصق الفنان الراحل في القاعة", "صورة", "نعم", "لا", "لا", "نعم", "نعم", None, "صورة مولَّدة بالذكاء الاصطناعي", "AI-generated image", "رئيسة التحرير"],
        ["دليل صوتي بصوت اصطناعي", "صوت", "لا", "لا", "لا", "نعم", "نعم", None, "يقرأ هذا الدليلَ صوتٌ اصطناعي؛ النص من إعداد القيّم", "This guide is read by a synthetic voice; text by the curator", "القيّم"],
        ["عرض فني بوجه ممثل مولَّد", "فيديو", "نعم", "نعم", "لا", "نعم", "نعم", None, "يتضمن العرض مشاهد مولَّدة بالذكاء الاصطناعي", "This work contains AI-generated scenes", "المخرجة"],
    ])
    for r in range(2, 101):
        ws[f"H{r}"] = (f'=IF(A{r}="","",IF(C{r}="نعم",IF(D{r}="نعم","إفصاح مناسب لا يعيق عرض العمل",'
                       f'"إفصاح واضح: محتوى مولَّد أو معدَّل (تزييف عميق)"),'
                       f'IF(E{r}="نعم",IF(AND(F{r}="نعم",G{r}="نعم"),"الاستثناء قد ينطبق؛ وثّق المراجعة والمسؤول",'
                       f'"إفصاح مطلوب: نص مولَّد"),"لا واجب في المادة ٥٠؛ قرّر وفق سياسة المؤسسة")))')
        ws[f"H{r}"].alignment = Alignment(wrap_text=True, horizontal="right", vertical="top")
    choices(ws, "C2:G100", ["نعم", "لا"])
    choices(ws, "B2:B100", ["نص", "صورة", "صوت", "فيديو"])
    flag(ws, "H2:H100", 'LEFT($H2,5)="إفصاح"', "FFF3D6")
    wb.save(path)


# ---------------------------------------------------------------- digital risk
def impact_recovery(path, color):
    wb = Workbook()
    intro(wb, color, "تحليل الأثر وأهداف الاستعادة", [
        "١. سجّل العمليات التي لا يجوز أن تتوقف، ومن يملك قرارها.",
        "٢. حدّد لكل عملية أقصى انقطاع مقبول بالدقائق (RTO) وأقصى فقد مقبول للبيانات (RPO).",
        "٣. بعد كل تمرين استعادة أدخل الزمن الفعلي وعمر النسخة؛ تقارن الورقة النتيجة بالهدف تلقائياً.",
    ])
    ws = sheet(wb, "العمليات الحرجة", color,
               ["العملية", "المالك", "RTO هدف زمن الاستعادة (دقيقة)", "RPO أقصى فقد للبيانات (دقيقة)",
                "زمن الاستعادة في التمرين", "عمر آخر نسخة عند الانقطاع", "نتيجة الزمن", "نتيجة البيانات", "تاريخ التمرين"],
               [24, 16, 18, 18, 18, 18, 18, 18, 14], [
                   ["حجوزات المهرجان", "مسؤولة الاستقبال", 60, 120, 65, 90, None, None, None],
                   ["بوابة الدفع", "المدير المالي", 30, 15, None, None, None, None, None],
                   ["البريد المؤسسي", "مسؤول التقنية", 240, 60, None, None, None, None, None],
               ])
    for r in range(2, 51):
        ws[f"G{r}"] = f'=IF(E{r}="","لم يُختبر",IF(E{r}<=C{r},"ضمن الهدف","تجاوز بـ "&(E{r}-C{r})&" دقيقة"))'
        ws[f"H{r}"] = f'=IF(F{r}="","لم يُختبر",IF(F{r}<=D{r},"ضمن الهدف","فقد أكبر من المقبول"))'
        ws[f"I{r}"].number_format = "yyyy-mm-dd"
    flag(ws, "G2:H50", 'OR(LEFT(G2,3)="تجا",LEFT(G2,3)="فقد")')
    flag(ws, "G2:H50", 'G2="لم يُختبر"', "FFF3D6")
    wb.save(path)


def payment_verification(path, color):
    wb = Workbook()
    intro(wb, color, "سجل التحقق من طلبات الدفع", [
        "القاعدة: أي مستفيد جديد أو تغيير في بيانات الحساب يُتحقق منه بالاتصال على رقم مسجّل مسبقاً، لا على رقم ورد في الطلب.",
        "أي مبلغ فوق الحد يحتاج معتمدَين. ويُحتجز التحويل لمستفيد جديد ٢٤ ساعة؛ يحسب السجل موعد انتهاء الاحتجاز.",
        "العجلة والسرية معاً إشارة إنذار. يحق لأي موظف رفض طلب مخالف للإجراء دون أن يُحاسب.",
        "إذا خرج مال بالخطأ: اتصل بالمصرف فوراً لمحاولة إيقاف التحويل، ثم أبلغ الإدارة.",
    ])
    ws = sheet(wb, "السجل", color,
               ["تاريخ الطلب ووقته", "مقدّم الطلب كما ظهر", "القناة", "المبلغ", "مستفيد جديد أو حساب معدَّل؟",
                "مصدر رقم الاتصال العكسي", "نتيجة الاتصال العكسي", "المعتمد الأول", "المعتمد الثاني",
                "ينتهي الاحتجاز في", "يحتاج معتمدَين؟", "القرار"],
               [18, 20, 14, 12, 16, 24, 18, 14, 14, 18, 14, 16], [
                   [None, "«المديرة التنفيذية»", "مكالمة فيديو", 48000, "نعم", "رقم العقد", "نفت المديرة الطلب", "المدير المالي", "", None, None, "مرفوض — بلاغ"],
               ])
    ws["N1"] = "حد المعتمدَين"
    ws["N1"].font = Font(name=FONT, bold=True)
    ws["O1"] = 5000
    ws["O1"].number_format = "#,##0"
    from datetime import datetime
    ws["A2"] = datetime(2026, 11, 24, 10, 15)
    for r in range(2, 201):
        ws[f"A{r}"].number_format = "yyyy-mm-dd hh:mm"
        ws[f"J{r}"] = f'=IF(OR(A{r}="",E{r}<>"نعم"),"",A{r}+1)'
        ws[f"J{r}"].number_format = "yyyy-mm-dd hh:mm"
        ws[f"K{r}"] = f'=IF(D{r}="","",IF(D{r}>$O$1,"نعم","لا"))'
        ws[f"D{r}"].number_format = "#,##0"
    choices(ws, "C2:C200", ["بريد", "هاتف", "مكالمة فيديو", "رسالة فورية", "حضوري"])
    choices(ws, "E2:E200", ["نعم", "لا"])
    choices(ws, "F2:F200", ["رقم العقد", "الدليل الداخلي", "رقم ورد في الطلب"])
    choices(ws, "L2:L200", ["معتمد بعد التحقق", "محتجز", "مرفوض — بلاغ"])
    flag(ws, "F2:F200", 'F2="رقم ورد في الطلب"')
    flag(ws, "I2:I200", 'AND(K2="نعم",I2="")', "FFF3D6")

    sheet(wb, "قائمة التحقق", color, ["قبل أي تحويل", "تم؟"], [70, 10], [
        ["هل المستفيد معروف ومسجّل سابقاً، دون تغيير في بيانات الحساب؟", ""],
        ["إن كان جديداً: هل اتصلتُ على رقم من العقد أو الدليل الداخلي، لا من الرسالة؟", ""],
        ["هل المبلغ فوق الحد؟ إذن هل وقّع المعتمد الثاني؟", ""],
        ["هل انقضت مدة الاحتجاز للمستفيد الجديد؟", ""],
        ["هل في الطلب عجلة وسرية معاً؟ إذن أبطئ وأبلغ المسؤول.", ""],
        ["هل حسابا البريد والمصرف محميّان بمصادقة مقاومة للتصيّد (مفاتيح FIDO أو مفاتيح المرور)؟", ""],
    ])
    choices(wb["قائمة التحقق"], "B2:B20", ["نعم", "لا"])
    wb.save(path)


BUILDERS = {
    "proposal_writing": [("funding-plan.xlsx", funding_plan), ("indicator-card.xlsx", indicator_card)],
    "ai_cultural_work": [("claim-log.xlsx", claim_log), ("disclosure-matrix.xlsx", disclosure_matrix)],
    "digital_safety": [("impact-recovery.xlsx", impact_recovery), ("payment-verification.xlsx", payment_verification)],
}

if __name__ == "__main__":
    for key, items in BUILDERS.items():
        folder = OUT / key
        folder.mkdir(parents=True, exist_ok=True)
        for name, build in items:
            build(folder / name, COLORS[key])
            print(folder / name)
