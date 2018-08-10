from EmailExtractor import app
from EmailExtractor.forms import FileForm, TextAreaForm, EmailForm
from EmailExtractor.logic import allowed_file, process_data, check_mx_record, check_mail_server, extract_emails_from_text
from flask import render_template, request


# Extract email addresses from text
@app.route('/', methods=['GET', 'POST'])
@app.route('/home', methods=['GET', 'POST'])
def home():
    # Assign empty string to emails to prevent any errors every time the if statement does not trigger
    emails = ''
    form = TextAreaForm()
    if form.validate_on_submit():
        # get text from submitted form
        text = request.form['text']
        # extract_emails_from_text() returns list of extracted emails
        emails = extract_emails_from_text(text)
    return render_template('home.html', form=form, emails=emails, length=len(emails))


@app.route('/upload_file', methods=['GET', 'POST'])
def upload_file():
    # Assign empty string to both variables to prevent any errors every time the if statement does not trigger
    verified_emails = ''
    emails_with_valid_format = ''

    # Create FileForm() object
    form = FileForm()
    # Check if input was submitted and validated
    if form.validate_on_submit():
        # get file from submitted form
        file = request.files['file']
        # Check if file is not None and has an allowed file extension
        if file and allowed_file(file.filename):
            # Catch UnicodeDecodeErrors in case the submitted file is not a txt or csv file
            try:
                # get file extension from file
                file_extension = file.filename.rsplit('.', 1)[1].lower()
                # process_data() returns a list of emails with valid address formats and a list of verified emails
                verified_emails, emails_with_valid_format = process_data(file.read().decode('utf-8'), file_extension)
            except UnicodeDecodeError:
                verified_emails = 'Text and CSV Files only!'
    return render_template('upload.html', form=form, valid_emails=verified_emails, valid_formats=emails_with_valid_format)


@app.route('/email_verifier.html', methods=['GET', 'POST'])
def email_verifier():
    check1 = False
    check2 = False
    form = EmailForm()
    if form.validate_on_submit():
        email = request.form['email']
        if check_mx_record(email):
            check1 = True
        if check_mx_record(email) and check_mail_server(email):
            check2 = True
    return render_template('email_verifier.html', form=form, check1=check1, check2=check2)

