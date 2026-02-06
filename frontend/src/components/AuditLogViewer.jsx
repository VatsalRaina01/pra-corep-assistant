import { useState } from 'react';

export default function AuditLogViewer({ queryId, justifications }) {
    const [expandedIndex, setExpandedIndex] = useState(null);

    const toggleExpand = (index) => {
        setExpandedIndex(expandedIndex === index ? null : index);
    };

    return (
        <div className="bg-surface rounded-lg p-6 border border-surface-light fade-in">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold flex items-center gap-2">
                    <svg className="w-5 h-5 text-primary" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd" />
                    </svg>
                    Audit Trail
                </h2>
                <span className="text-xs font-mono text-text-muted">
                    ID: {queryId.substring(0, 8)}...
                </span>
            </div>

            {justifications.length === 0 ? (
                <div className="text-center py-8 text-text-muted">
                    <p>No justifications available</p>
                </div>
            ) : (
                <div className="space-y-3">
                    {justifications.map((just, index) => (
                        <div
                            key={index}
                            className="bg-background rounded-lg border border-surface-light overflow-hidden"
                        >
                            <button
                                onClick={() => toggleExpand(index)}
                                className="w-full px-4 py-3 flex items-center justify-between hover:bg-surface-light/30 transition-colors"
                            >
                                <div className="flex items-center gap-3">
                                    <span className="text-xs font-mono text-text-muted bg-surface-light px-2 py-1 rounded">
                                        {just.field_id}
                                    </span>
                                    <span className="text-sm font-medium text-text">
                                        {just.rule_references.length} rule reference{just.rule_references.length !== 1 ? 's' : ''}
                                    </span>
                                    <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${just.confidence >= 0.8 ? 'bg-secondary/10 text-secondary' :
                                            just.confidence >= 0.6 ? 'bg-warning/10 text-warning' :
                                                'bg-error/10 text-error'
                                        }`}>
                                        {(just.confidence * 100).toFixed(0)}%
                                    </span>
                                </div>
                                <svg
                                    className={`w-5 h-5 text-text-muted transition-transform ${expandedIndex === index ? 'rotate-180' : ''
                                        }`}
                                    fill="none"
                                    stroke="currentColor"
                                    viewBox="0 0 24 24"
                                >
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                </svg>
                            </button>

                            {expandedIndex === index && (
                                <div className="px-4 pb-4 space-y-3 border-t border-surface-light">
                                    {/* Reasoning */}
                                    <div className="pt-3">
                                        <h4 className="text-xs font-semibold text-text-muted mb-2">LLM Reasoning</h4>
                                        <p className="text-sm text-text leading-relaxed bg-surface-light/30 rounded p-3">
                                            {just.reasoning}
                                        </p>
                                    </div>

                                    {/* Rule References */}
                                    <div>
                                        <h4 className="text-xs font-semibold text-text-muted mb-2">Regulatory References</h4>
                                        <div className="space-y-2">
                                            {just.rule_references.map((ref, refIndex) => (
                                                <div
                                                    key={refIndex}
                                                    className="bg-surface-light/30 rounded p-3 border-l-2 border-primary"
                                                >
                                                    <div className="flex items-center justify-between mb-2">
                                                        <span className="text-xs font-semibold text-primary">
                                                            {ref.source} - {ref.article}
                                                            {ref.paragraph && ` (${ref.paragraph})`}
                                                        </span>
                                                        <span className="text-xs text-text-muted">
                                                            Relevance: {(ref.relevance_score * 100).toFixed(0)}%
                                                        </span>
                                                    </div>
                                                    <p className="text-xs text-text-muted leading-relaxed">
                                                        {ref.text_excerpt}
                                                    </p>
                                                </div>
                                            ))}
                                        </div>
                                    </div>
                                </div>
                            )}
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
