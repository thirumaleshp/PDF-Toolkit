from flask import Flask, render_template, request, send_file, jsonify, redirect, url_for
import os
import tempfile
import uuid
from werkzeug.utils import secure_filename
from pdf_utils import PDFToolkit

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB max file size
app.config['UPLOAD_FOLDER'] = tempfile.gettempdir()

pdf_toolkit = PDFToolkit()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/merge', methods=['POST'])
def merge_pdfs():
    if 'files' not in request.files:
        return jsonify({'error': 'No files provided'}), 400
    
    files = request.files.getlist('files')
    if len(files) < 2:
        return jsonify({'error': 'At least 2 PDF files are required for merging'}), 400
    
    # Save uploaded files temporarily
    temp_files = []
    try:
        for file in files:
            if file.filename == '':
                continue
            
            if file and file.filename.lower().endswith('.pdf'):
                filename = secure_filename(file.filename)
                temp_path = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}_{filename}")
                file.save(temp_path)
                temp_files.append(temp_path)
        
        if len(temp_files) < 2:
            return jsonify({'error': 'At least 2 valid PDF files are required'}), 400
        
        # Create output file
        output_filename = f"merged_{uuid.uuid4()}.pdf"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Merge PDFs
        success = pdf_toolkit.merge_pdfs(temp_files, output_path)
        
        if success:
            return send_file(output_path, as_attachment=True, download_name='merged.pdf')
        else:
            return jsonify({'error': 'Failed to merge PDF files'}), 500
    
    except Exception as e:
        return jsonify({'error': f'Error processing files: {str(e)}'}), 500
    
    finally:
        # Clean up temporary files
        for temp_file in temp_files:
            try:
                os.remove(temp_file)
            except:
                pass

@app.route('/api/convert', methods=['POST'])
def convert_file():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not pdf_toolkit.is_supported_format(file.filename):
        supported = pdf_toolkit.get_supported_formats()
        return jsonify({
            'error': 'Unsupported file format',
            'supported_formats': supported
        }), 400
    
    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_input = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}_{filename}")
        file.save(temp_input)
        
        # Create output file
        output_filename = f"{os.path.splitext(filename)[0]}_{uuid.uuid4()}.pdf"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Convert to PDF
        success = pdf_toolkit.convert_to_pdf(temp_input, output_path)
        
        if success:
            return send_file(output_path, as_attachment=True, 
                           download_name=f"{os.path.splitext(filename)[0]}.pdf")
        else:
            return jsonify({'error': 'Failed to convert file to PDF'}), 500
    
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500
    
    finally:
        # Clean up temporary input file
        try:
            os.remove(temp_input)
        except:
            pass

@app.route('/api/split', methods=['POST'])
def split_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '' or not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Please provide a valid PDF file'}), 400
    
    page_ranges = request.form.get('page_ranges', '')
    if not page_ranges:
        return jsonify({'error': 'Page ranges are required'}), 400
    
    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_input = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}_{filename}")
        file.save(temp_input)
        
        # Create output file
        output_filename = f"split_{os.path.splitext(filename)[0]}_{uuid.uuid4()}.pdf"
        output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
        
        # Split PDF
        success = pdf_toolkit.split_pdf(temp_input, page_ranges, output_path, combine_pages=True)
        
        if success:
            return send_file(output_path, as_attachment=True, 
                           download_name=f"split_{os.path.splitext(filename)[0]}.pdf")
        else:
            return jsonify({'error': 'Failed to split PDF'}), 500
    
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500
    
    finally:
        # Clean up temporary input file
        try:
            os.remove(temp_input)
        except:
            pass

@app.route('/api/export', methods=['POST'])
def export_pdf():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '' or not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Please provide a valid PDF file'}), 400
    
    export_format = request.form.get('format', '')
    if export_format not in ['word', 'excel', 'powerpoint', 'images']:
        return jsonify({'error': 'Invalid export format. Supported: word, excel, powerpoint, images'}), 400
    
    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_input = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}_{filename}")
        file.save(temp_input)
        
        base_name = os.path.splitext(filename)[0]
        
        if export_format == 'word':
            output_filename = f"{base_name}_{uuid.uuid4()}.docx"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            success = pdf_toolkit.convert_pdf_to_word(temp_input, output_path)
            download_name = f"{base_name}.docx"
            
        elif export_format == 'excel':
            output_filename = f"{base_name}_{uuid.uuid4()}.xlsx"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            success = pdf_toolkit.convert_pdf_to_excel(temp_input, output_path)
            download_name = f"{base_name}.xlsx"
            
        elif export_format == 'powerpoint':
            output_filename = f"{base_name}_{uuid.uuid4()}.pptx"
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], output_filename)
            success = pdf_toolkit.convert_pdf_to_powerpoint(temp_input, output_path)
            download_name = f"{base_name}.pptx"
            
        elif export_format == 'images':
            # Get PDF info to check page count
            pdf_info = pdf_toolkit.get_pdf_info(temp_input)
            if pdf_info['page_count'] == 1:
                # Single page - return single image
                output_dir = os.path.join(app.config['UPLOAD_FOLDER'], f"{base_name}_{uuid.uuid4()}_images")
                success = pdf_toolkit.convert_pdf_to_images(temp_input, output_dir, 'png')
                if success:
                    image_files = [f for f in os.listdir(output_dir) if f.endswith('.png')]
                    if image_files:
                        output_path = os.path.join(output_dir, image_files[0])
                        download_name = f"{base_name}.png"
                    else:
                        success = False
            else:
                # Multiple pages - create ZIP file
                import zipfile
                output_dir = os.path.join(app.config['UPLOAD_FOLDER'], f"{base_name}_{uuid.uuid4()}_images")
                success = pdf_toolkit.convert_pdf_to_images(temp_input, output_dir, 'png')
                if success:
                    zip_filename = f"{base_name}_{uuid.uuid4()}_images.zip"
                    output_path = os.path.join(app.config['UPLOAD_FOLDER'], zip_filename)
                    with zipfile.ZipFile(output_path, 'w') as zip_file:
                        for image_file in os.listdir(output_dir):
                            if image_file.endswith('.png'):
                                zip_file.write(os.path.join(output_dir, image_file), image_file)
                    download_name = f"{base_name}_images.zip"
        
        if success:
            return send_file(output_path, as_attachment=True, download_name=download_name)
        else:
            return jsonify({'error': f'Failed to export PDF to {export_format}'}), 500
    
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500
    
    finally:
        # Clean up temporary input file
        try:
            os.remove(temp_input)
        except:
            pass

@app.route('/api/pdf-info', methods=['POST'])
def get_pdf_info():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '' or not file.filename.lower().endswith('.pdf'):
        return jsonify({'error': 'Please provide a valid PDF file'}), 400
    
    try:
        # Save uploaded file temporarily
        filename = secure_filename(file.filename)
        temp_input = os.path.join(app.config['UPLOAD_FOLDER'], f"{uuid.uuid4()}_{filename}")
        file.save(temp_input)
        
        # Get PDF info
        info = pdf_toolkit.get_pdf_info(temp_input)
        
        return jsonify(info)
    
    except Exception as e:
        return jsonify({'error': f'Error processing file: {str(e)}'}), 500
    
    finally:
        # Clean up temporary input file
        try:
            os.remove(temp_input)
        except:
            pass

@app.route('/api/supported-formats')
def get_supported_formats():
    return jsonify(pdf_toolkit.get_supported_formats())

if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    templates_dir = os.path.join(os.path.dirname(__file__), 'templates')
    if not os.path.exists(templates_dir):
        os.makedirs(templates_dir)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
