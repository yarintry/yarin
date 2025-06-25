from flask import Flask, request, send_file, render_template, redirect, url_for
import pandas as pd
from docx import Document
import WordPrint as wp
import os

app = Flask(__name__)

@app.route('/')
def upload_form():
    return render_template('upload.html')

@app.route('/convert', methods=['GET'])
def convert_get():
    return redirect(url_for('upload_form'))

@app.route('/convert', methods=['POST'])
def convert():
    file = request.files['file']
    mastab = request.form.get('mastab', '').strip()
    division = request.form.get('division', '').strip()
    unit = request.form.get('unit', '').strip()
    action = request.form.get('action')

    excel_path = 'uploaded.xlsx'
    word_path = 'output.docx'

    file.save(excel_path)
    df = pd.read_excel(excel_path)

    if action == 'convert':
        convert_excel_to_word(df, word_path)
        return send_file(word_path, as_attachment=True)

    elif action == 'filter_by_mastab':
        filtered = filter_by_values(df, mastab, division, unit)
        if filtered.empty:
            return render_template(
                'upload.html',
                message="לא נמצאו תוצאות לסינון שבוצע"
            )
        convert_excel_to_word(filtered, word_path)
        return send_file(word_path, as_attachment=True)

    else:
        return "שגיאה: פעולה לא מזוהה", 400


def convert_excel_to_word(df, word_file):
    doc = Document('tofestov.docx')
    wp.excelEctract(doc, df)
    doc.save(word_file)


# פונקציית סינון כללית לפי עמודות (בהתאם למה שהוזן)
def filter_by_values(df, mastab=None, division=None, unit=None):
    try:
        filtered = df.copy()

        # בדוק האם העמודות קיימות
        columns = df.columns.str.lower()

        # אתחל משתנים עם שמות העמודות הרלוונטיים
        mastab_col = None
        division_col = None
        unit_col = None

        # חפש עמודות תואמות לפי שם (בלי רגישות לאותיות)
        for col in df.columns:
            lower_col = col.lower()
            if 'מסטב' in lower_col or 'mastab' in lower_col:
                mastab_col = col
            elif 'חטיבה' in lower_col or 'division' in lower_col:
                division_col = col
            elif 'מסגרת' in lower_col or 'unit' in lower_col:
                unit_col = col

        if mastab and mastab_col:
            filtered = filtered[filtered[mastab_col].astype(str).str.strip().str.lower() == mastab.strip().lower()]
        if division and division_col:
            filtered = filtered[filtered[division_col].astype(str).str.strip().str.lower() == division.strip().lower()]
        if unit and unit_col:
            filtered = filtered[filtered[unit_col].astype(str).str.strip().str.lower() == unit.strip().lower()]

        return filtered

    except Exception as e:
        print(f"שגיאה בסינון: {e}")
        return pd.DataFrame()


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

