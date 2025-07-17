# All-in-One File Converter

A completely client-side file conversion tool that works directly in your browser. No server required!

## Features

- **Image Converter**: Convert between PNG, JPG, WEBP, HEIC formats
- **Image to PDF**: Convert single or multiple images to PDF
- **DOCX to PDF**: Convert Word documents to PDF
- **Excel to PDF**: Convert spreadsheets to PDF  
- **PDF Merge**: Combine multiple PDFs into one
- **PDF Split**: Extract specific pages from PDFs

## Privacy & Security

- All conversions happen locally in your browser
- No files are uploaded to any server
- Your documents never leave your device
- Works completely offline after initial load

## Deployment

This is a static web application that can be deployed anywhere:

### Option 1: GitHub Pages
1. Create a new repository on GitHub
2. Upload `index.html` to the repository
3. Go to Settings > Pages
4. Select source branch and deploy

### Option 2: Netlify
1. Go to [netlify.com](https://netlify.com)
2. Drag and drop the `index.html` file
3. Your app will be live instantly

### Option 3: Vercel
1. Go to [vercel.com](https://vercel.com)
2. Import your project or upload the file
3. Deploy with one click

### Option 4: Local Testing
1. Open `index.html` in any modern web browser
2. The app works immediately - no server needed!

## Browser Support

Works in all modern browsers that support:
- HTML5 Canvas
- FileReader API
- Web Workers (for PDF processing)

## Libraries Used

- [jsPDF](https://github.com/parallax/jsPDF) - PDF generation
- [PDF-lib](https://github.com/Hopding/pdf-lib) - PDF manipulation
- [mammoth.js](https://github.com/mwilliamson/mammoth.js) - DOCX to HTML conversion
- [SheetJS](https://github.com/SheetJS/sheetjs) - Excel file processing
- [heic2any](https://github.com/alexcorvi/heic2any) - HEIC/HEIF conversion
- [html2canvas](https://github.com/niklasvh/html2canvas) - HTML to image conversion
- [JSZip](https://github.com/Stuk/jszip) - ZIP file handling
- [Tailwind CSS](https://tailwindcss.com) - Styling

## License

MIT License - feel free to use and modify!
