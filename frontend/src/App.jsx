import { useState } from 'react';
import axios from 'axios';
import QueryForm from './components/QueryForm';
import TemplateViewer from './components/TemplateViewer';
import ValidationPanel from './components/ValidationPanel';
import AuditLogViewer from './components/AuditLogViewer';
import ReasoningViewer from './components/ReasoningViewer';

function App() {
    const [loading, setLoading] = useState(false);
    const [response, setResponse] = useState(null);
    const [error, setError] = useState(null);
    const [streamingProgress, setStreamingProgress] = useState(0);
    const [streamingStatus, setStreamingStatus] = useState('');
    const [reasoningSteps, setReasoningSteps] = useState(null);
    const [useStreaming, setUseStreaming] = useState(true);

    const handleSubmit = async (queryData) => {
        setLoading(true);
        setError(null);
        setResponse(null);
        setStreamingProgress(0);
        setStreamingStatus('');
        setReasoningSteps(null);

        if (useStreaming) {
            handleStreamingSubmit(queryData);
        } else {
            handleNormalSubmit(queryData);
        }
    };

    const handleStreamingSubmit = async (queryData) => {
        try {
            const response = await fetch('/api/query/stream', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(queryData),
            });

            const reader = response.body.getReader();
            const decoder = new TextDecoder();

            while (true) {
                const { done, value } = await reader.read();
                if (done) break;

                const chunk = decoder.decode(value);
                const lines = chunk.split('\n');

                for (const line of lines) {
                    if (line.startsWith('data: ')) {
                        const data = JSON.parse(line.slice(6));

                        switch (data.type) {
                            case 'start':
                                setStreamingStatus('Starting...');
                                break;

                            case 'status':
                                setStreamingStatus(data.message);
                                setStreamingProgress(data.progress);
                                break;

                            case 'reasoning':
                                // Accumulate reasoning content
                                setStreamingStatus('Generating reasoning...');
                                break;

                            case 'partial_result':
                                // Show partial results as they come in
                                setStreamingProgress(data.progress);
                                break;

                            case 'complete':
                                // Final result
                                setReasoningSteps(data.data.reasoning_steps);
                                setResponse({
                                    query_id: data.data.query_id || 'streaming',
                                    template_id: queryData.template_id,
                                    fields: data.data.fields,
                                    justifications: data.data.justifications,
                                    validation: { is_valid: true, errors: [], warnings: [] }
                                });
                                break;

                            case 'validation':
                                // Update validation results
                                setResponse(prev => ({
                                    ...prev,
                                    validation: data.data
                                }));
                                setStreamingProgress(data.progress);
                                break;

                            case 'done':
                                setLoading(false);
                                setStreamingProgress(100);
                                setStreamingStatus('Complete!');
                                break;

                            case 'error':
                                setError(data.message);
                                setLoading(false);
                                break;
                        }
                    }
                }
            }
        } catch (err) {
            setError(err.message || 'An error occurred during streaming');
            setLoading(false);
        }
    };

    const handleNormalSubmit = async (queryData) => {
        try {
            const result = await axios.post('/api/query', queryData);
            setResponse(result.data);
        } catch (err) {
            setError(err.response?.data?.detail || 'An error occurred processing your query');
            console.error('Query error:', err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-background">
            {/* Header */}
            <header className="bg-surface border-b border-surface-light">
                <div className="max-w-7xl mx-auto px-6 py-4">
                    <div className="flex items-center justify-between">
                        <div>
                            <h1 className="text-2xl font-bold bg-gradient-to-r from-primary to-secondary bg-clip-text text-transparent">
                                PRA COREP Assistant
                            </h1>
                            <p className="text-sm text-text-muted mt-1">
                                LLM-assisted regulatory reporting with streaming & chain-of-thought
                            </p>
                        </div>
                        <div className="flex items-center gap-4">
                            {/* Streaming Toggle */}
                            <label className="flex items-center gap-2 cursor-pointer">
                                <input
                                    type="checkbox"
                                    checked={useStreaming}
                                    onChange={(e) => setUseStreaming(e.target.checked)}
                                    className="w-4 h-4 text-primary bg-background border-surface-light rounded focus:ring-primary"
                                />
                                <span className="text-sm text-text-muted">
                                    Streaming Mode
                                </span>
                            </label>

                            <div className="flex items-center gap-2 px-3 py-1.5 bg-secondary/10 rounded-full">
                                <div className="w-2 h-2 bg-secondary rounded-full animate-pulse"></div>
                                <span className="text-xs text-secondary font-medium">Operational</span>
                            </div>
                        </div>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-6 py-8">
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Left Column - Query Form */}
                    <div className="space-y-6">
                        <QueryForm onSubmit={handleSubmit} loading={loading} />

                        {/* Streaming Progress */}
                        {loading && useStreaming && (
                            <div className="bg-surface rounded-lg p-4 border border-surface-light fade-in">
                                <div className="flex items-center justify-between mb-2">
                                    <span className="text-sm font-medium text-text">{streamingStatus}</span>
                                    <span className="text-sm text-text-muted">{streamingProgress}%</span>
                                </div>
                                <div className="w-full bg-background rounded-full h-2">
                                    <div
                                        className="bg-gradient-to-r from-primary to-secondary h-2 rounded-full transition-all duration-300"
                                        style={{ width: `${streamingProgress}%` }}
                                    ></div>
                                </div>
                            </div>
                        )}

                        {error && (
                            <div className="bg-error/10 border border-error/30 rounded-lg p-4 fade-in">
                                <div className="flex items-start gap-3">
                                    <svg className="w-5 h-5 text-error flex-shrink-0 mt-0.5" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                                    </svg>
                                    <div>
                                        <h3 className="font-semibold text-error">Error</h3>
                                        <p className="text-sm text-error/90 mt-1">{error}</p>
                                    </div>
                                </div>
                            </div>
                        )}
                    </div>

                    {/* Right Column - Results */}
                    <div className="space-y-6">
                        {loading && !useStreaming && (
                            <div className="bg-surface rounded-lg p-8 text-center fade-in">
                                <div className="inline-block w-12 h-12 border-4 border-primary/30 border-t-primary rounded-full animate-spin"></div>
                                <p className="text-text-muted mt-4">Processing your query...</p>
                                <p className="text-sm text-text-muted/70 mt-2">
                                    Retrieving regulatory text and generating COREP output
                                </p>
                            </div>
                        )}

                        {response && !loading && (
                            <>
                                {/* Chain-of-Thought Reasoning */}
                                {reasoningSteps && (
                                    <ReasoningViewer reasoningSteps={reasoningSteps} />
                                )}

                                <TemplateViewer
                                    templateId={response.template_id}
                                    fields={response.fields}
                                />

                                <ValidationPanel validation={response.validation} />

                                <AuditLogViewer
                                    queryId={response.query_id}
                                    justifications={response.justifications}
                                />
                            </>
                        )}

                        {!response && !loading && !error && (
                            <div className="bg-surface rounded-lg p-8 text-center border border-surface-light">
                                <svg className="w-16 h-16 mx-auto text-text-muted/30" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                                <h3 className="text-lg font-semibold text-text-muted mt-4">No Results Yet</h3>
                                <p className="text-sm text-text-muted/70 mt-2">
                                    Enter a query to generate COREP template output
                                </p>
                                {useStreaming && (
                                    <p className="text-xs text-primary mt-2">
                                        ⚡ Streaming mode enabled - see real-time progress
                                    </p>
                                )}
                            </div>
                        )}
                    </div>
                </div>
            </main>

            {/* Footer */}
            <footer className="mt-16 border-t border-surface-light">
                <div className="max-w-7xl mx-auto px-6 py-6">
                    <p className="text-center text-sm text-text-muted">
                        PRA COREP Assistant v1.0 • Advanced Features: Streaming, Chain-of-Thought, Validation, Audit Trail
                    </p>
                </div>
            </footer>
        </div>
    );
}

export default App;
