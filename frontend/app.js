/**
 * PRA COREP Assistant - Enhanced Frontend
 * Handles chat and analyze modes with template population
 */

// ============================================================================
// Configuration
// ============================================================================

const API_BASE_URL = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : 'https://pra-corep-api.onrender.com';

// ============================================================================
// State
// ============================================================================

let currentMode = 'chat';
let conversationHistory = [];
let isProcessing = false;
let lastAnalysisResult = null;

// ============================================================================
// DOM Elements
// ============================================================================

const elements = {
    chatContainer: document.getElementById('chat-container'),
    analyzeContainer: document.getElementById('analyze-container'),
    messages: document.getElementById('messages'),
    welcomeMessage: document.getElementById('welcome-message'),
    messageInput: document.getElementById('message-input'),
    sendButton: document.getElementById('send-button'),
    charCount: document.getElementById('char-count'),
    statusIndicator: document.getElementById('status-indicator'),
    statusText: document.querySelector('.status-text'),
    modeHint: document.getElementById('mode-hint'),
    templateSelect: document.getElementById('template-select'),
    resultsPanel: document.getElementById('results-panel'),
    analyzePlaceholder: document.getElementById('analyze-placeholder'),
    templateTitle: document.getElementById('template-title'),
    templateBody: document.getElementById('template-body'),
    totalsContent: document.getElementById('totals-content'),
    validationContent: document.getElementById('validation-content'),
    auditContent: document.getElementById('audit-content'),
    exportPdfBtn: document.getElementById('export-pdf-btn')
};

// ============================================================================
// Initialization
// ============================================================================

document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();
    checkHealth();
    autoResizeTextarea();
});

function setupEventListeners() {
    // Mode toggle
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.addEventListener('click', () => switchMode(btn.dataset.mode));
    });

    // Send message
    elements.sendButton.addEventListener('click', handleSend);
    elements.messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSend();
        }
    });

    // Auto-resize and char count
    elements.messageInput.addEventListener('input', () => {
        autoResizeTextarea();
        updateCharCount();
    });

    // Export PDF
    elements.exportPdfBtn?.addEventListener('click', exportPdf);
}

function autoResizeTextarea() {
    const textarea = elements.messageInput;
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 150) + 'px';
}

function updateCharCount() {
    elements.charCount.textContent = elements.messageInput.value.length;
}

// ============================================================================
// Mode Switching
// ============================================================================

function switchMode(mode) {
    currentMode = mode;

    // Update buttons
    document.querySelectorAll('.mode-btn').forEach(btn => {
        btn.classList.toggle('active', btn.dataset.mode === mode);
    });

    // Show/hide containers
    elements.chatContainer.style.display = mode === 'chat' ? 'block' : 'none';
    elements.analyzeContainer.style.display = mode === 'analyze' ? 'flex' : 'none';

    // Update hint
    elements.modeHint.textContent = mode === 'chat'
        ? 'Press Enter to send'
        : 'Describe your capital scenario';

    // Update placeholder
    elements.messageInput.placeholder = mode === 'chat'
        ? 'Ask about COREP templates, capital requirements, or validation rules...'
        : 'Describe your bank\'s capital position (e.g., share capital, reserves, RWA)...';
}

// ============================================================================
// API Functions
// ============================================================================

async function checkHealth() {
    try {
        const response = await fetch(`${API_BASE_URL}/health`);
        if (response.ok) {
            setStatus('connected');
        } else {
            setStatus('error');
        }
    } catch (error) {
        console.error('Health check failed:', error);
        setStatus('error');
    }
}

async function handleSend() {
    const message = elements.messageInput.value.trim();
    if (!message || isProcessing) return;

    elements.messageInput.value = '';
    autoResizeTextarea();
    updateCharCount();

    if (currentMode === 'chat') {
        await sendChatMessage(message);
    } else {
        await analyzeScenario(message);
    }
}

async function sendChatMessage(message) {
    if (elements.welcomeMessage) {
        elements.welcomeMessage.style.display = 'none';
    }

    addMessage('user', message);
    conversationHistory.push({ role: 'user', content: message });

    await streamResponse(message);
}

async function streamResponse(message) {
    isProcessing = true;
    setStatus('loading');
    elements.sendButton.disabled = true;

    const messageElement = addMessage('assistant', '');
    const contentElement = messageElement.querySelector('.message-content');
    contentElement.innerHTML = `<div class="typing-indicator"><span></span><span></span><span></span></div>`;

    let fullResponse = '';

    try {
        const response = await fetch(`${API_BASE_URL}/chat/stream`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                message: message,
                history: conversationHistory.slice(0, -1)
            })
        });

        if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        contentElement.innerHTML = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value);
            const lines = chunk.split('\n');

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = line.substring(6);
                    if (data === '[DONE]') break;

                    try {
                        const parsed = JSON.parse(data);
                        if (parsed.content) {
                            fullResponse += parsed.content;
                            contentElement.innerHTML = renderMarkdown(fullResponse);
                            scrollToBottom();
                        }
                        if (parsed.error) throw new Error(parsed.error);
                    } catch (e) {
                        if (e.message !== 'Unexpected end of JSON input') {
                            console.error('Parse error:', e);
                        }
                    }
                }
            }
        }

        if (fullResponse) {
            conversationHistory.push({ role: 'assistant', content: fullResponse });
        }
        setStatus('connected');

    } catch (error) {
        console.error('Stream error:', error);
        contentElement.innerHTML = `
            <p style="color: var(--error);">Error: ${error.message}</p>
        `;
        setStatus('error');
    } finally {
        isProcessing = false;
        elements.sendButton.disabled = false;
        elements.messageInput.focus();
    }
}

async function analyzeScenario(scenario) {
    isProcessing = true;
    setStatus('loading');
    elements.sendButton.disabled = true;

    const template = elements.templateSelect.value;

    try {
        const response = await fetch(`${API_BASE_URL}/analyze`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ scenario, template })
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Analysis failed');
        }

        const result = await response.json();
        lastAnalysisResult = { scenario, template };
        renderAnalysisResult(result);
        setStatus('connected');

    } catch (error) {
        console.error('Analysis error:', error);
        alert(`Analysis failed: ${error.message}`);
        setStatus('error');
    } finally {
        isProcessing = false;
        elements.sendButton.disabled = false;
        elements.messageInput.focus();
    }
}

async function exportPdf() {
    if (!lastAnalysisResult) {
        alert('Please run an analysis first');
        return;
    }

    setStatus('loading');

    try {
        const response = await fetch(`${API_BASE_URL}/export/pdf`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(lastAnalysisResult)
        });

        if (!response.ok) throw new Error('PDF export failed');

        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `COREP_${lastAnalysisResult.template}_${new Date().toISOString().slice(0, 10)}.pdf`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        window.URL.revokeObjectURL(url);

        setStatus('connected');

    } catch (error) {
        console.error('Export error:', error);
        alert(`Export failed: ${error.message}`);
        setStatus('error');
    }
}

// ============================================================================
// Rendering Functions
// ============================================================================

function renderAnalysisResult(result) {
    // Show results panel
    elements.analyzePlaceholder.style.display = 'none';
    elements.resultsPanel.style.display = 'grid';

    // Update title
    elements.templateTitle.textContent = `${result.template_id} - ${result.template_name}`;

    // Render template table
    renderTemplateTable(result.fields, result.totals);

    // Render totals and ratios
    renderTotals(result.totals, result.ratios);

    // Render validation
    renderValidation(result.validation_results);

    // Render audit trail
    renderAuditTrail(result.audit_trail);
}

function renderTemplateTable(fields, totals) {
    let html = '';

    for (const field of fields) {
        const isTotal = field.row_id === '200' || field.row_id === '400' ||
            field.row_id === '500' || field.row_id === '700' ||
            field.row_id === '800' || field.row_id === '050' ||
            field.row_id === '150';

        const value = field.value;
        const valueClass = value === null ? '' : (field.sign === '-' ? 'negative' : 'positive');
        const valueStr = value !== null ? formatNumber(value) : '—';

        html += `
            <tr class="${isTotal ? 'row-total' : ''}">
                <td class="row-id">${field.row_id}</td>
                <td>${field.label}</td>
                <td class="row-value ${valueClass}">${field.sign === '-' ? '-' : ''}${valueStr}</td>
            </tr>
        `;
    }

    elements.templateBody.innerHTML = html;
}

function renderTotals(totals, ratios) {
    let html = '';

    // Capital totals
    const capitalItems = [
        { key: 'cet1', label: 'CET1 Capital' },
        { key: 'at1', label: 'AT1 Capital' },
        { key: 'tier1', label: 'Tier 1 Capital' },
        { key: 'tier2', label: 'Tier 2 Capital' },
        { key: 'total_own_funds', label: 'Total Own Funds' }
    ];

    for (const item of capitalItems) {
        if (totals[item.key] !== undefined) {
            html += `
                <div class="totals-item">
                    <span class="label">${item.label}</span>
                    <span class="value">£${formatNumber(totals[item.key])}m</span>
                </div>
            `;
        }
    }

    // Ratios
    if (ratios && Object.keys(ratios).length > 0) {
        html += '<div style="border-top: 1px solid var(--border-color); margin: 8px 0;"></div>';

        const ratioItems = [
            { key: 'cet1_ratio', label: 'CET1 Ratio' },
            { key: 'tier1_ratio', label: 'Tier 1 Ratio' },
            { key: 'total_capital_ratio', label: 'Total Capital Ratio' }
        ];

        for (const item of ratioItems) {
            if (ratios[item.key] !== undefined) {
                html += `
                    <div class="totals-item ratio">
                        <span class="label">${item.label}</span>
                        <span class="value">${ratios[item.key]}%</span>
                    </div>
                `;
            }
        }
    }

    elements.totalsContent.innerHTML = html;
}

function renderValidation(results) {
    let html = '';

    for (const result of results) {
        const statusClass = result.passed ? 'pass' : (result.severity === 'WARNING' ? 'warning' : 'fail');
        const icon = result.passed ? '✓' : (result.severity === 'WARNING' ? '⚠' : '✗');

        html += `
            <div class="validation-item ${statusClass}">
                <span class="validation-icon">${icon}</span>
                <div class="validation-text">
                    <div class="name">${result.name}</div>
                    <div class="message">${result.message}</div>
                </div>
            </div>
        `;
    }

    elements.validationContent.innerHTML = html || '<p style="color: var(--text-tertiary);">No validation results</p>';
}

function renderAuditTrail(auditTrail) {
    let html = '';

    for (const item of auditTrail) {
        html += `
            <div class="audit-item">
                <div class="field">Row ${item.field}</div>
                <div class="rule">${item.rule_title}</div>
                <div class="explanation">${item.explanation}</div>
            </div>
        `;
    }

    elements.auditContent.innerHTML = html || '<p style="color: var(--text-tertiary);">No audit trail available</p>';
}

function addMessage(role, content) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const avatar = role === 'assistant'
        ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5z"/><path d="M2 17l10 5 10-5"/><path d="M2 12l10 5 10-5"/></svg>'
        : '👤';

    messageDiv.innerHTML = `
        <div class="message-avatar">${avatar}</div>
        <div class="message-content">${role === 'user' ? escapeHtml(content) : renderMarkdown(content)}</div>
    `;

    elements.messages.appendChild(messageDiv);
    scrollToBottom();
    return messageDiv;
}

function scrollToBottom() {
    elements.chatContainer.scrollTop = elements.chatContainer.scrollHeight;
}

function setStatus(status) {
    elements.statusIndicator.className = `status-indicator ${status}`;
    elements.statusText.textContent = {
        connected: 'Connected',
        loading: 'Processing...',
        error: 'Disconnected'
    }[status];
}

// ============================================================================
// Utility Functions
// ============================================================================

function formatNumber(num) {
    if (num === null || num === undefined) return '—';
    return num.toLocaleString('en-GB', { minimumFractionDigits: 0, maximumFractionDigits: 2 });
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

function renderMarkdown(text) {
    let html = escapeHtml(text);

    // Code blocks
    html = html.replace(/```(\w+)?\n([\s\S]*?)```/g, '<pre><code>$2</code></pre>');
    html = html.replace(/`([^`]+)`/g, '<code>$1</code>');

    // Bold and italic
    html = html.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
    html = html.replace(/\*([^*]+)\*/g, '<em>$1</em>');

    // Headers
    html = html.replace(/^### (.+)$/gm, '<h3>$1</h3>');
    html = html.replace(/^## (.+)$/gm, '<h2>$1</h2>');
    html = html.replace(/^# (.+)$/gm, '<h1>$1</h1>');

    // Lists
    html = html.replace(/^\s*[-*] (.+)$/gm, '<li>$1</li>');
    html = html.replace(/(<li>.*<\/li>\n?)+/g, '<ul>$&</ul>');
    html = html.replace(/^\s*\d+\. (.+)$/gm, '<li>$1</li>');

    // Paragraphs
    html = html.split('\n\n').map(p => {
        if (p.startsWith('<h') || p.startsWith('<ul') || p.startsWith('<ol') || p.startsWith('<pre')) {
            return p;
        }
        return `<p>${p}</p>`;
    }).join('');

    html = html.replace(/<p><\/p>/g, '');
    html = html.replace(/\n/g, '<br>');
    html = html.replace(/<br><br>/g, '<br>');

    return html;
}
