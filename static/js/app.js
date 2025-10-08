/**
 * Spectral Clip Forge - Frontend JavaScript
 * The forge's interactive enchantments
 */

(function() {
    'use strict';

    // State
    let selectedFile = null;
    let currentJobId = null;

    // DOM Elements
    const uploadZone = document.getElementById('upload-zone');
    const fileInput = document.getElementById('file-input');
    const fileInfo = document.getElementById('file-info');
    const uploadBtn = document.getElementById('upload-btn');
    const progressSection = document.getElementById('progress-section');
    const progressFill = document.getElementById('progress-fill');
    const progressText = document.getElementById('progress-text');
    const statusSection = document.getElementById('status-section');
    const statusContent = document.getElementById('status-content');

    // Initialize
    function init() {
        setupEventListeners();
    }

    // Setup Event Listeners
    function setupEventListeners() {
        if (uploadZone) {
            uploadZone.addEventListener('click', () => fileInput.click());
            uploadZone.addEventListener('dragover', handleDragOver);
            uploadZone.addEventListener('drop', handleDrop);
        }

        if (fileInput) {
            fileInput.addEventListener('change', handleFileSelect);
        }

        if (uploadBtn) {
            uploadBtn.addEventListener('click', handleUpload);
        }
    }

    // Handle drag over
    function handleDragOver(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadZone.style.borderColor = 'var(--spectral-neon)';
        uploadZone.style.background = 'rgba(123, 44, 191, 0.2)';
    }

    // Handle drop
    function handleDrop(e) {
        e.preventDefault();
        e.stopPropagation();
        uploadZone.style.borderColor = 'var(--spectral-purple)';
        uploadZone.style.background = 'rgba(123, 44, 191, 0.05)';

        const files = e.dataTransfer.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    }

    // Handle file selection
    function handleFileSelect(e) {
        const files = e.target.files;
        if (files.length > 0) {
            handleFile(files[0]);
        }
    }

    // Handle file
    function handleFile(file) {
        selectedFile = file;

        // Validate file
        validateFile(file).then(isValid => {
            if (isValid) {
                displayFileInfo(file);
                uploadBtn.disabled = false;
            } else {
                alert('Invalid file. Please select a valid media file.');
                selectedFile = null;
            }
        });
    }

    // Validate file
    async function validateFile(file) {
        try {
            const response = await fetch('/api/upload/validate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    filename: file.name,
                    size: file.size
                })
            });

            const data = await response.json();
            return data.valid;
        } catch (error) {
            console.error('Validation error:', error);
            return false;
        }
    }

    // Display file info
    function displayFileInfo(file) {
        document.getElementById('filename').textContent = file.name;
        document.getElementById('filesize').textContent = formatFileSize(file.size);
        fileInfo.style.display = 'block';
    }

    // Format file size
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
    }

    // Handle upload
    async function handleUpload() {
        if (!selectedFile) {
            alert('Please select a file first');
            return;
        }

        // Get selected formats
        const formatCheckboxes = document.querySelectorAll('input[name="format"]:checked');
        const formats = Array.from(formatCheckboxes).map(cb => cb.value);

        if (formats.length === 0) {
            alert('Please select at least one target format');
            return;
        }

        // Get options
        const watermark = document.querySelector('input[name="watermark"]').checked;
        const effects = document.querySelector('input[name="effects"]:checked')?.value || 'spectral';

        // Prepare form data
        const formData = new FormData();
        formData.append('file', selectedFile);
        formats.forEach(format => formData.append('formats', format));
        formData.append('watermark', watermark);
        formData.append('effects', effects);

        // Show progress
        uploadBtn.disabled = true;
        progressSection.style.display = 'block';
        progressText.textContent = 'Uploading to the forge...';

        try {
            const response = await fetch('/api/upload/', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            if (response.ok) {
                currentJobId = data.job_id;
                progressText.textContent = '✨ Upload complete! Forging begins...';
                progressFill.style.width = '100%';

                // Start polling for status
                setTimeout(() => {
                    pollJobStatus(currentJobId);
                }, 2000);
            } else {
                throw new Error(data.message || 'Upload failed');
            }
        } catch (error) {
            console.error('Upload error:', error);
            alert('Upload failed: ' + error.message);
            resetUploadForm();
        }
    }

    // Poll job status
    async function pollJobStatus(jobId) {
        try {
            const response = await fetch(`/api/process/${jobId}`);
            const data = await response.json();

            if (response.ok) {
                displayJobStatus(data.job);

                // Continue polling if still processing
                if (data.job.status === 'pending' || data.job.status === 'processing') {
                    setTimeout(() => pollJobStatus(jobId), 3000);
                }
            } else {
                throw new Error('Failed to get job status');
            }
        } catch (error) {
            console.error('Status polling error:', error);
        }
    }

    // Display job status
    function displayJobStatus(job) {
        statusSection.style.display = 'block';
        
        let statusHTML = `
            <div class="job-status-display">
                <p><strong>Job ID:</strong> ${job.id}</p>
                <p><strong>File:</strong> ${job.filename}</p>
                <p><strong>Status:</strong> <span class="status-${job.status}">${job.status.toUpperCase()}</span></p>
                <p><strong>Target Formats:</strong> ${job.target_formats.join(', ')}</p>
        `;

        if (job.status === 'processing') {
            statusHTML += `
                <div class="processing-animation">
                    <p>🔥 The forge is burning hot... Your clips are being crafted... 🔥</p>
                </div>
            `;
        } else if (job.status === 'completed') {
            statusHTML += `
                <div class="completion-message">
                    <p>✨ The forging is complete! Your legendary artifacts await! ✨</p>
                    <p><strong>Processing Time:</strong> ${job.processing_time?.toFixed(2)} seconds</p>
                    <div class="download-links">
                        <h4>Download Your Clips:</h4>
            `;

            job.output_files.forEach(file => {
                statusHTML += `
                    <a href="/api/download/${job.id}/${file}" class="download-btn">${file}</a>
                `;
            });

            statusHTML += `
                        <a href="/api/download/${job.id}/all" class="download-btn forge-button">Download All (ZIP)</a>
                    </div>
                </div>
            `;

            // Reset form for new upload
            setTimeout(resetUploadForm, 1000);
        } else if (job.status === 'failed') {
            statusHTML += `
                <div class="error-message">
                    <p>❌ The forge encountered an error:</p>
                    <p><strong>${job.error_message || 'Unknown error'}</strong></p>
                    <button class="forge-button" onclick="location.reload()">Try Again</button>
                </div>
            `;
        }

        statusHTML += '</div>';
        statusContent.innerHTML = statusHTML;
    }

    // Reset upload form
    function resetUploadForm() {
        selectedFile = null;
        fileInput.value = '';
        fileInfo.style.display = 'none';
        progressSection.style.display = 'none';
        progressFill.style.width = '0%';
        uploadBtn.disabled = true;
    }

    // Initialize on DOM ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
