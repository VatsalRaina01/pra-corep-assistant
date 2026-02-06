export default function TemplateViewer({ templateId, fields }) {
    const getConfidenceColor = (confidence) => {
        if (confidence >= 0.8) return 'text-secondary';
        if (confidence >= 0.6) return 'text-warning';
        return 'text-error';
    };

    const getConfidenceBg = (confidence) => {
        if (confidence >= 0.8) return 'bg-secondary/10';
        if (confidence >= 0.6) return 'bg-warning/10';
        return 'bg-error/10';
    };

    return (
        <div className="bg-surface rounded-lg p-6 border border-surface-light fade-in">
            <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold flex items-center gap-2">
                    <svg className="w-5 h-5 text-secondary" fill="currentColor" viewBox="0 0 20 20">
                        <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                        <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm3 4a1 1 0 000 2h.01a1 1 0 100-2H7zm3 0a1 1 0 000 2h3a1 1 0 100-2h-3zm-3 4a1 1 0 100 2h.01a1 1 0 100-2H7zm3 0a1 1 0 100 2h3a1 1 0 100-2h-3z" clipRule="evenodd" />
                    </svg>
                    COREP Template {templateId}
                </h2>
                <span className="text-xs px-2 py-1 bg-primary/10 text-primary rounded-full font-medium">
                    Own Funds
                </span>
            </div>

            {fields.length === 0 ? (
                <div className="text-center py-8 text-text-muted">
                    <p>No fields populated</p>
                </div>
            ) : (
                <div className="space-y-3">
                    {fields.map((field, index) => (
                        <div
                            key={index}
                            className="bg-background rounded-lg p-4 border border-surface-light hover:border-primary/30 transition-colors"
                        >
                            <div className="flex items-start justify-between">
                                <div className="flex-1">
                                    <div className="flex items-center gap-2 mb-1">
                                        <span className="text-xs font-mono text-text-muted">
                                            Row {field.row} • Col {field.column}
                                        </span>
                                        <span className={`text-xs px-2 py-0.5 rounded-full font-medium ${getConfidenceBg(field.confidence)} ${getConfidenceColor(field.confidence)}`}>
                                            {(field.confidence * 100).toFixed(0)}% confidence
                                        </span>
                                    </div>
                                    <h3 className="font-semibold text-text mb-2">{field.label}</h3>
                                    <div className="flex items-baseline gap-2">
                                        <span className="text-2xl font-bold text-primary">
                                            £{field.value?.toLocaleString()}
                                        </span>
                                        <span className="text-sm text-text-muted">thousands</span>
                                    </div>
                                </div>
                                <div className="flex-shrink-0">
                                    <svg className="w-8 h-8 text-secondary/20" fill="currentColor" viewBox="0 0 20 20">
                                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                                    </svg>
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
