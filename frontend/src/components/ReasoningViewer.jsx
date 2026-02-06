export default function ReasoningViewer({ reasoningSteps }) {
    if (!reasoningSteps) return null;

    const steps = [
        { key: 'analysis', label: 'Step 1: Analysis', icon: '🔍', color: 'primary' },
        { key: 'calculation', label: 'Step 2: Calculation', icon: '🧮', color: 'secondary' },
        { key: 'justification', label: 'Step 3: Justification', icon: '📋', color: 'warning' },
        { key: 'verification', label: 'Step 4: Verification', icon: '✅', color: 'success' }
    ];

    return (
        <div className="bg-surface rounded-lg p-6 border border-surface-light fade-in">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <svg className="w-5 h-5 text-primary" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9 2a1 1 0 000 2h2a1 1 0 100-2H9z" />
                    <path fillRule="evenodd" d="M4 5a2 2 0 012-2 3 3 0 003 3h2a3 3 0 003-3 2 2 0 012 2v11a2 2 0 01-2 2H6a2 2 0 01-2-2V5zm9.707 5.707a1 1 0 00-1.414-1.414L9 12.586l-1.293-1.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                </svg>
                Chain-of-Thought Reasoning
            </h2>

            <div className="space-y-4">
                {steps.map((step, index) => (
                    reasoningSteps[step.key] && (
                        <div
                            key={step.key}
                            className="bg-background rounded-lg p-4 border-l-4 border-primary"
                        >
                            <div className="flex items-start gap-3">
                                <span className="text-2xl">{step.icon}</span>
                                <div className="flex-1">
                                    <h3 className="font-semibold text-text mb-2">{step.label}</h3>
                                    <p className="text-sm text-text-muted leading-relaxed whitespace-pre-wrap">
                                        {reasoningSteps[step.key]}
                                    </p>
                                </div>
                            </div>
                        </div>
                    )
                ))}
            </div>

            <div className="mt-4 p-3 bg-primary/10 rounded-lg border border-primary/30">
                <p className="text-xs text-primary">
                    💡 This chain-of-thought reasoning shows how the LLM analyzed the regulatory context
                    and arrived at the final COREP values step-by-step.
                </p>
            </div>
        </div>
    );
}
