import React, { useEffect } from 'react';
import { defaultLayoutPlugin } from '@react-pdf-viewer/default-layout';
import { Worker, Viewer } from '@react-pdf-viewer/core';
import '@react-pdf-viewer/core/lib/styles/index.css';
import '@react-pdf-viewer/default-layout/lib/styles/index.css';

const PDFViewer = ({ pdfUrl }) => {
  const pdfPath = `http://localhost:8001/nova/ai-fi/api/v1/webservices/document-management/download/${pdfUrl}`;
  const newplugin = defaultLayoutPlugin();

  useEffect(() => {
    console.log('PDFViewer component mounted');
    console.log('PDF Path:', pdfPath);

    return () => {
      console.log('PDFViewer component unmounted');
    };
  }, [pdfPath]);

  return (
    <div style={{ height: '100%', width: '100%' }}>
      <Worker workerUrl="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.16.105/pdf.worker.min.js">
        <Viewer plugins={[newplugin]}
          fileUrl={pdfPath}
          onError={(error) => {
            console.error('Error loading PDF:', error);
            alert('Error loading PDF. Check console for details.');
          }}
          onLoadSuccess={() => console.log('PDF loaded successfully')}
          onLoadError={(error) => console.error('Error during PDF load:', error)}
          onSourceError={(error) => console.error('Error with PDF source:', error)}
        />
      </Worker>
    </div>
  );
};

export default PDFViewer;