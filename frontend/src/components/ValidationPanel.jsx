export default function ValidationPanel({ validation }) {
    if (!validation) return null;

    const hasIssues = validation.errors.length > 0 || validation.warnings.length > 0;

    return (
        <div className="bg-surface rounded-lg p-6 border border-surface-light fade-in">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <svg className="w-5 h-5 text-warning" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Validation Results
            </h2>

            {!hasIssues ? (
                <div className="bg-secondary/10 border border-secondary/30 rounded-lg p-4">
                    <div className="flex items-center gap-3">
                        <svg className="w-6 h-6 text-secondary flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
                            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                        </svg>
                        <div>
                            <h3 className="font-semibold text-secondary">All Checks Passed</h3>
                            <p className="text-sm text-secondary/80 mt-1">
                                No validation errors or warnings detected
                            </p>
                        </div>
                    </div>
                </div>
            ) : (
                <div className="space-y-3">
                    {/* Errors */}
                    {validation.errors.length > 0 && (
                        <div className="space-y-2">
                            <h3 className="text-sm font-semibold text-error flex items-center gap-2">
                                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                                </svg>
                                Errors ({validation.errors.length})
                            </h3>
                            {validation.errors.map((error, index) => (
                                <div key={index} className="bg-error/10 border border-error/30 rounded-lg p-3">
                                    <div className="flex items-start gap-2">
                                        <span className="text-xs font-mono text-error/70 mt-0.5">
                                            {error.field_id || 'GENERAL'}
                                        </span>
                                        <div className="flex-1">
                                            <p className="text-sm text-error">{error.message}</p>
                                            {error.rule && (
                                                <p className="text-xs text-error/60 mt-1">Rule: {error.rule}</p>
                                            )}
                                        </div>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}

                    {/* Warnings */}
                    {validation.warnings.length > 0 && (
                        <div className="space-y-2">
                            <h3 className="text-sm font-semibold text-warning flex items-center gap-2">
                                <svg className="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                                    <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                                </svg>
                                Warnings ({validation.warnings.length})
                            </h3>
                            {validation.warnings.map((warning, index) => (
                                <div key={index} className="bg-warning/10 border border-warning/30 rounded-lg p-3">
                                    <div className="flex items-start gap-2">
                                        <span className="text-xs font-mono text-warning/70 mt-0.5">
                                            {warning.field_id || 'GENERAL'}
                                        </span>
                                        <p className="text-sm text-warning flex-1">{warning.message}</p>
                                    </div>
                                </div>
                            ))}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
}
