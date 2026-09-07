/**
 * Smart Applicant - Frontend Application Logic
 * ============================================
 * Handles Drag & Drop, Async REST API calls, Dynamic UI updates,
 * Score animations, Keyword pills, History management, and Presets.
 */

document.addEventListener('DOMContentLoaded', () => {
    // DOM Elements
    const analyzerForm = document.getElementById('analyzerForm');
    const resumeInput = document.getElementById('resumeInput');
    const dropZone = document.getElementById('dropZone');
    const dropZoneContent = document.getElementById('dropZoneContent');
    const filePreview = document.getElementById('filePreview');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const btnRemoveFile = document.getElementById('btnRemoveFile');

    const jobDescription = document.getElementById('jobDescription');
    const charCounter = document.getElementById('charCounter');
    const btnClearJD = document.getElementById('btnClearJD');
    const presetButtons = document.querySelectorAll('.preset-btn');

    const btnSubmit = document.getElementById('btnSubmit');
    const btnSubmitText = document.getElementById('btnSubmitText');
    const btnLoadingSpinner = document.getElementById('btnLoadingSpinner');

    // Results Elements
    const resultsSection = document.getElementById('resultsSection');
    const resultJobTitle = document.getElementById('resultJobTitle');
    const scoreCirclePath = document.getElementById('scoreCirclePath');
    const scoreValue = document.getElementById('scoreValue');
    const scoreBadge = document.getElementById('scoreBadge');
    const scoreDescription = document.getElementById('scoreDescription');
    const metricFoundCount = document.getElementById('metricFoundCount');
    const metricMissingCount = document.getElementById('metricMissingCount');
    const pillFoundCounter = document.getElementById('pillFoundCounter');
    const pillMissingCounter = document.getElementById('pillMissingCounter');
    const foundKeywordsContainer = document.getElementById('foundKeywordsContainer');
    const missingKeywordsContainer = document.getElementById('missingKeywordsContainer');
    const recommendationsContainer = document.getElementById('recommendationsContainer');

    const btnPrintReport = document.getElementById('btnPrintReport');
    const btnScrollToTop = document.getElementById('btnScrollToTop');

    // History Modal Elements
    const btnOpenHistory = document.getElementById('btnOpenHistory');
    const btnCloseHistory = document.getElementById('btnCloseHistory');
    const historyModal = document.getElementById('historyModal');
    const historyModalBackdrop = document.getElementById('historyModalBackdrop');
    const historyListContainer = document.getElementById('historyListContainer');
    const historyBadge = document.getElementById('historyBadge');

    // Algorithm Modal Elements
    const btnOpenAlgorithm = document.getElementById('btnOpenAlgorithm');
    const btnCloseAlgo = document.getElementById('btnCloseAlgo');
    const btnCloseAlgoBottom = document.getElementById('btnCloseAlgoBottom');
    const algorithmModal = document.getElementById('algorithmModal');
    const algoModalBackdrop = document.getElementById('algoModalBackdrop');

    const toastContainer = document.getElementById('toastContainer');

    let currentFile = null;

    // ------------------------------------------------------------------------
    // Toast Notification Helper
    // ------------------------------------------------------------------------
    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        toast.className = `pointer-events-auto flex items-center gap-3 px-4 py-3 rounded-xl shadow-2xl text-sm font-medium border toast-enter ${
            type === 'success' ? 'bg-emerald-950/90 text-emerald-200 border-emerald-700/80' :
            type === 'error' ? 'bg-rose-950/90 text-rose-200 border-rose-700/80' :
            type === 'warning' ? 'bg-amber-950/90 text-amber-200 border-amber-700/80' :
            'bg-slate-800/90 text-slate-200 border-slate-700'
        }`;

        const iconClass = type === 'success' ? 'fa-circle-check text-emerald-400' :
                          type === 'error' ? 'fa-circle-exclamation text-rose-400' :
                          type === 'warning' ? 'fa-triangle-exclamation text-amber-400' :
                          'fa-circle-info text-blue-400';

        toast.innerHTML = `
            <i class="fa-solid ${iconClass} text-base flex-shrink-0"></i>
            <span>${message}</span>
        `;

        toastContainer.appendChild(toast);
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(10px)';
            toast.style.transition = 'all 0.3s ease';
            setTimeout(() => toast.remove(), 300);
        }, 4000);
    }

    // ------------------------------------------------------------------------
    // File Drag & Drop Handling
    // ------------------------------------------------------------------------
    function handleFile(file) {
        if (!file) return;

        if (file.type !== 'application/pdf' && !file.name.toLowerCase().endsWith('.pdf')) {
            showToast('Only standard PDF files are supported.', 'error');
            return;
        }

        if (file.size > 16 * 1024 * 1024) {
            showToast('File size exceeds the 16MB limit.', 'error');
            return;
        }

        currentFile = file;
        fileName.textContent = file.name;
        fileSize.textContent = (file.size / 1024).toFixed(1) + ' KB';

        dropZoneContent.classList.add('hidden');
        filePreview.classList.remove('hidden');
        dropZone.classList.remove('drag-active');
        showToast(`Selected "${file.name}"`, 'success');
    }

    function clearFile() {
        currentFile = null;
        resumeInput.value = '';
        dropZoneContent.classList.remove('hidden');
        filePreview.classList.add('hidden');
    }

    resumeInput.addEventListener('change', (e) => {
        if (e.target.files && e.target.files[0]) {
            handleFile(e.target.files[0]);
        }
    });

    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.add('drag-active');
        });
    });

    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, (e) => {
            e.preventDefault();
            e.stopPropagation();
            dropZone.classList.remove('drag-active');
        });
    });

    dropZone.addEventListener('drop', (e) => {
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0]);
        }
    });

    btnRemoveFile.addEventListener('click', (e) => {
        e.stopPropagation();
        clearFile();
    });

    // ------------------------------------------------------------------------
    // Job Description & Presets
    // ------------------------------------------------------------------------
    jobDescription.addEventListener('input', () => {
        const count = jobDescription.value.trim().length;
        charCounter.textContent = `${count} characters`;
    });

    btnClearJD.addEventListener('click', () => {
        jobDescription.value = '';
        charCounter.textContent = '0 characters';
    });

    presetButtons.forEach(btn => {
        btn.addEventListener('click', async () => {
            const presetType = btn.getAttribute('data-preset');
            try {
                btn.disabled = true;
                const res = await fetch(`/api/sample-job/${presetType}`);
                const data = await res.json();
                if (data.success) {
                    jobDescription.value = data.content;
                    charCounter.textContent = `${data.content.length} characters`;
                    showToast(`Loaded ${btn.textContent.trim()} preset`, 'info');
                }
            } catch (err) {
                showToast('Failed to load sample job description', 'error');
            } finally {
                btn.disabled = false;
            }
        });
    });

    // ------------------------------------------------------------------------
    // Form Submission & Analysis
    // ------------------------------------------------------------------------
    analyzerForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        if (!currentFile) {
            showToast('Please upload a PDF resume before analyzing.', 'warning');
            return;
        }

        const jdText = jobDescription.value.trim();
        if (!jdText || jdText.length < 20) {
            showToast('Please enter a sufficiently detailed job description (minimum 20 characters).', 'warning');
            jobDescription.focus();
            return;
        }

        // Setup UI loading state
        btnSubmit.disabled = true;
        btnSubmitText.classList.add('hidden');
        btnLoadingSpinner.classList.remove('hidden');
        btnLoadingSpinner.classList.add('flex');

        const formData = new FormData();
        formData.append('resume', currentFile);
        formData.append('job_description', jdText);

        try {
            const response = await fetch('/api/analyze', {
                method: 'POST',
                body: formData
            });

            const result = await response.json();

            if (!response.ok || !result.success) {
                throw new Error(result.error || 'Failed to process resume.');
            }

            // Render Result
            renderAnalysisReport(result);
            showToast('Analysis completed successfully!', 'success');
            refreshHistoryCount();

        } catch (error) {
            showToast(error.message, 'error');
        } finally {
            btnSubmit.disabled = false;
            btnSubmitText.classList.remove('hidden');
            btnLoadingSpinner.classList.add('hidden');
            btnLoadingSpinner.classList.remove('flex');
        }
    });

    // ------------------------------------------------------------------------
    // Render Results & Animations
    // ------------------------------------------------------------------------
    function renderAnalysisReport(data) {
        resultsSection.classList.remove('hidden');

        // Scroll smoothly to results
        resultsSection.scrollIntoView({ behavior: 'smooth', block: 'start' });

        // Update Job Title
        resultJobTitle.innerHTML = `Target Role: <span class="text-slate-200 font-semibold">${data.job_title}</span> • Resume File: <span class="text-slate-300 font-mono text-xs">${data.filename}</span>`;

        // Animate Score Gauge
        animateScore(data.match_score);

        // Update Counts
        metricFoundCount.textContent = data.total_found_count;
        metricMissingCount.textContent = data.total_missing_count;
        pillFoundCounter.textContent = `${data.total_found_count} matched`;
        pillMissingCounter.textContent = `${data.total_missing_count} missing`;

        // Render Found Keywords (Green Pills)
        foundKeywordsContainer.innerHTML = '';
        if (data.found_keywords && data.found_keywords.length > 0) {
            data.found_keywords.forEach(keyword => {
                const pill = document.createElement('span');
                pill.className = 'inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-emerald-500/15 text-emerald-300 border border-emerald-500/30 hover:bg-emerald-500/25 transition';
                pill.innerHTML = `<i class="fa-solid fa-check text-[10px] text-emerald-400"></i> ${escapeHtml(keyword)}`;
                foundKeywordsContainer.appendChild(pill);
            });
        } else {
            foundKeywordsContainer.innerHTML = '<p class="text-xs text-slate-500 italic">No significant matching keywords detected.</p>';
        }

        // Render Missing Keywords (Red Pills)
        missingKeywordsContainer.innerHTML = '';
        if (data.missing_keywords && data.missing_keywords.length > 0) {
            data.missing_keywords.forEach(keyword => {
                const pill = document.createElement('span');
                pill.className = 'inline-flex items-center gap-1.5 px-3 py-1 rounded-full text-xs font-semibold bg-rose-500/15 text-rose-300 border border-rose-500/30 hover:bg-rose-500/25 transition';
                pill.innerHTML = `<i class="fa-solid fa-plus text-[10px] text-rose-400"></i> ${escapeHtml(keyword)}`;
                missingKeywordsContainer.appendChild(pill);
            });
        } else {
            missingKeywordsContainer.innerHTML = '<p class="text-xs text-emerald-400 font-medium">Outstanding! All primary job keywords were identified in your resume.</p>';
        }

        // Render Recommendations Cards
        recommendationsContainer.innerHTML = '';
        if (data.recommendations && data.recommendations.length > 0) {
            data.recommendations.forEach(rec => {
                const card = document.createElement('div');
                const theme = getRecTheme(rec.type);
                card.className = `p-4 rounded-xl border ${theme.bg} ${theme.border} space-y-1`;
                card.innerHTML = `
                    <div class="flex items-center gap-2">
                        <i class="fa-solid ${theme.icon} ${theme.textColor} text-sm"></i>
                        <h4 class="text-sm font-bold text-slate-200">${escapeHtml(rec.title)}</h4>
                    </div>
                    <p class="text-xs text-slate-300 leading-relaxed pl-5">${rec.text}</p>
                `;
                recommendationsContainer.appendChild(card);
            });
        }
    }

    function animateScore(targetScore) {
        let current = 0;
        const duration = 1200;
        const start = performance.now();

        // Color & Category based on score
        let strokeColor, badgeClass, badgeText, description;
        if (targetScore >= 75) {
            strokeColor = '#10b981'; // emerald
            badgeClass = 'bg-emerald-500/20 text-emerald-300 border-emerald-500/40';
            badgeText = 'Strong Match';
            description = 'High semantic and keyword resonance. The resume fulfills the major qualifications sought by the recruiter.';
        } else if (targetScore >= 50) {
            strokeColor = '#f59e0b'; // amber
            badgeClass = 'bg-amber-500/20 text-amber-300 border-amber-500/40';
            badgeText = 'Moderate Match';
            description = 'Good foundation, but several key technical skills are missing. Adding targeted terms will optimize your ranking.';
        } else {
            strokeColor = '#f43f5e'; // rose
            badgeClass = 'bg-rose-500/20 text-rose-300 border-rose-500/40';
            badgeText = 'Needs Improvement';
            description = 'Low keyword overlap. Significant gaps exist between this resume and the stated requirements.';
        }

        scoreCirclePath.style.color = strokeColor;
        scoreBadge.className = `inline-block px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider border ${badgeClass}`;
        scoreBadge.textContent = badgeText;
        scoreDescription.textContent = description;

        function update(now) {
            const elapsed = now - start;
            const progress = Math.min(elapsed / duration, 1);
            // Ease out cubic
            const easeProgress = 1 - Math.pow(1 - progress, 3);
            current = (targetScore * easeProgress);

            scoreValue.textContent = `${current.toFixed(1)}%`;
            scoreCirclePath.setAttribute('stroke-dasharray', `${current}, 100`);

            if (progress < 1) {
                requestAnimationFrame(update);
            } else {
                scoreValue.textContent = `${targetScore.toFixed(1)}%`;
                scoreCirclePath.setAttribute('stroke-dasharray', `${targetScore}, 100`);
            }
        }
        requestAnimationFrame(update);
    }

    function getRecTheme(type) {
        switch (type) {
            case 'success':
                return { bg: 'bg-emerald-950/40', border: 'border-emerald-700/50', textColor: 'text-emerald-400', icon: 'fa-circle-check' };
            case 'warning':
                return { bg: 'bg-amber-950/40', border: 'border-amber-700/50', textColor: 'text-amber-400', icon: 'fa-triangle-exclamation' };
            case 'danger':
                return { bg: 'bg-rose-950/40', border: 'border-rose-700/50', textColor: 'text-rose-400', icon: 'fa-circle-xmark' };
            case 'info':
            default:
                return { bg: 'bg-blue-950/40', border: 'border-blue-700/50', textColor: 'text-blue-400', icon: 'fa-circle-info' };
        }
    }

    // ------------------------------------------------------------------------
    // Print & Reset Actions
    // ------------------------------------------------------------------------
    btnPrintReport.addEventListener('click', () => {
        window.print();
    });

    btnScrollToTop.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // ------------------------------------------------------------------------
    // History Modal Management
    // ------------------------------------------------------------------------
    async function loadHistory() {
        historyListContainer.innerHTML = `
            <div class="text-center py-8 text-slate-400">
                <i class="fa-solid fa-spinner animate-spin text-xl mb-2"></i>
                <p class="text-xs">Loading database records...</p>
            </div>
        `;

        try {
            const res = await fetch('/api/history');
            const data = await res.json();

            if (!data.success || !data.history) {
                throw new Error('Failed to load history.');
            }

            historyBadge.textContent = data.history.length;

            if (data.history.length === 0) {
                historyListContainer.innerHTML = `
                    <div class="text-center py-10 text-slate-500">
                        <i class="fa-solid fa-folder-open text-3xl mb-2"></i>
                        <p class="text-xs">No analysis records stored in SQLite yet.</p>
                    </div>
                `;
                return;
            }

            historyListContainer.innerHTML = '';
            data.history.forEach(item => {
                const card = document.createElement('div');
                card.className = 'bg-slate-800/80 border border-slate-700 rounded-xl p-4 flex items-center justify-between gap-3 hover:border-slate-600 transition';

                const badgeBg = item.match_score >= 75 ? 'text-emerald-400 bg-emerald-500/15' :
                                item.match_score >= 50 ? 'text-amber-400 bg-amber-500/15' :
                                'text-rose-400 bg-rose-500/15';

                card.innerHTML = `
                    <div class="min-w-0 flex-1">
                        <div class="flex items-center gap-2">
                            <span class="text-xs px-2 py-0.5 rounded font-bold ${badgeBg}">${item.match_score}%</span>
                            <h4 class="text-sm font-semibold text-slate-200 truncate">${escapeHtml(item.job_title)}</h4>
                        </div>
                        <p class="text-xs text-slate-400 mt-1 truncate">
                            <i class="fa-solid fa-file-lines text-slate-500 mr-1"></i> ${escapeHtml(item.filename)}
                        </p>
                        <span class="text-[10px] text-slate-500 block mt-0.5">${item.created_at}</span>
                    </div>
                    <button data-id="${item.id}" class="btn-delete-history text-slate-500 hover:text-red-400 p-2 transition" title="Delete record">
                        <i class="fa-solid fa-trash-can text-sm"></i>
                    </button>
                `;
                historyListContainer.appendChild(card);
            });

            // Bind Delete Buttons
            document.querySelectorAll('.btn-delete-history').forEach(btn => {
                btn.addEventListener('click', async () => {
                    const id = btn.getAttribute('data-id');
                    try {
                        const delRes = await fetch(`/api/history/${id}`, { method: 'DELETE' });
                        const delData = await delRes.json();
                        if (delData.success) {
                            showToast('Record deleted.', 'info');
                            loadHistory();
                        }
                    } catch (e) {
                        showToast('Error deleting record.', 'error');
                    }
                });
            });

        } catch (e) {
            historyListContainer.innerHTML = '<p class="text-xs text-rose-400 text-center py-4">Failed to load history records.</p>';
        }
    }

    async function refreshHistoryCount() {
        try {
            const res = await fetch('/api/history');
            const data = await res.json();
            if (data.success && data.history) {
                historyBadge.textContent = data.history.length;
            }
        } catch (_) {}
    }

    btnOpenHistory.addEventListener('click', () => {
        historyModal.classList.remove('hidden');
        loadHistory();
    });

    btnCloseHistory.addEventListener('click', () => {
        historyModal.classList.add('hidden');
    });

    historyModalBackdrop.addEventListener('click', () => {
        historyModal.classList.add('hidden');
    });

    // ------------------------------------------------------------------------
    // Algorithm Modal
    // ------------------------------------------------------------------------
    btnOpenAlgorithm.addEventListener('click', () => {
        algorithmModal.classList.remove('hidden');
    });

    [btnCloseAlgo, btnCloseAlgoBottom, algoModalBackdrop].forEach(el => {
        if (el) {
            el.addEventListener('click', () => {
                algorithmModal.classList.add('hidden');
            });
        }
    });

    // Helper: HTML Escaping
    function escapeHtml(text) {
        if (!text) return '';
        const map = {
            '&': '&amp;',
            '<': '&lt;',
            '>': '&gt;',
            '"': '&quot;',
            "'": '&#039;'
        };
        return text.replace(/[&<>"']/g, m => map[m]);
    }

    // Initial count check
    refreshHistoryCount();
});
