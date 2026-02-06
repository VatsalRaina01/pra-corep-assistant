import { useState } from 'react';

export default function QueryForm({ onSubmit, loading }) {
    const [query, setQuery] = useState('');
    const [scenario, setScenario] = useState({
        entity_type: 'UK bank',
        ordinary_shares: '',
        retained_earnings: '',
        additional_tier1: '',
        tier2_capital: '',
        currency: 'GBP'
    });

    const handleSubmit = (e) => {
        e.preventDefault();

        // Convert string values to numbers
        const processedScenario = {
            ...scenario,
            ordinary_shares: parseFloat(scenario.ordinary_shares) || 0,
            retained_earnings: parseFloat(scenario.retained_earnings) || 0,
            additional_tier1: parseFloat(scenario.additional_tier1) || 0,
            tier2_capital: parseFloat(scenario.tier2_capital) || 0,
        };

        onSubmit({
            user_query: query,
            scenario: processedScenario,
            template_id: 'C_01_00'
        });
    };

    return (
        <div className="bg-surface rounded-lg p-6 border border-surface-light fade-in">
            <h2 className="text-xl font-semibold mb-4 flex items-center gap-2">
                <svg className="w-5 h-5 text-primary" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-8-3a1 1 0 00-.867.5 1 1 0 11-1.731-1A3 3 0 0113 8a3.001 3.001 0 01-2 2.83V11a1 1 0 11-2 0v-1a1 1 0 011-1 1 1 0 100-2zm0 8a1 1 0 100-2 1 1 0 000 2z" clipRule="evenodd" />
                </svg>
                Query Input
            </h2>

            <form onSubmit={handleSubmit} className="space-y-4">
                {/* Natural Language Query */}
                <div>
                    <label className="block text-sm font-medium mb-2">
                        Natural Language Question
                    </label>
                    <textarea
                        value={query}
                        onChange={(e) => setQuery(e.target.value)}
                        placeholder="e.g., How should we report Tier 1 capital for our UK subsidiary?"
                        className="w-full px-4 py-3 bg-background border border-surface-light rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-text placeholder-text-muted/50 resize-none"
                        rows={3}
                        required
                    />
                </div>

                {/* Scenario Details */}
                <div className="border-t border-surface-light pt-4">
                    <h3 className="text-sm font-medium mb-3 text-text-muted">Scenario Details (GBP Millions)</h3>

                    <div className="grid grid-cols-2 gap-3">
                        <div>
                            <label className="block text-xs font-medium mb-1.5 text-text-muted">
                                Ordinary Shares
                            </label>
                            <input
                                type="number"
                                value={scenario.ordinary_shares}
                                onChange={(e) => setScenario({ ...scenario, ordinary_shares: e.target.value })}
                                placeholder="500"
                                className="w-full px-3 py-2 bg-background border border-surface-light rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-text text-sm"
                            />
                        </div>

                        <div>
                            <label className="block text-xs font-medium mb-1.5 text-text-muted">
                                Retained Earnings
                            </label>
                            <input
                                type="number"
                                value={scenario.retained_earnings}
                                onChange={(e) => setScenario({ ...scenario, retained_earnings: e.target.value })}
                                placeholder="100"
                                className="w-full px-3 py-2 bg-background border border-surface-light rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-text text-sm"
                            />
                        </div>

                        <div>
                            <label className="block text-xs font-medium mb-1.5 text-text-muted">
                                Additional Tier 1
                            </label>
                            <input
                                type="number"
                                value={scenario.additional_tier1}
                                onChange={(e) => setScenario({ ...scenario, additional_tier1: e.target.value })}
                                placeholder="0"
                                className="w-full px-3 py-2 bg-background border border-surface-light rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-text text-sm"
                            />
                        </div>

                        <div>
                            <label className="block text-xs font-medium mb-1.5 text-text-muted">
                                Tier 2 Capital
                            </label>
                            <input
                                type="number"
                                value={scenario.tier2_capital}
                                onChange={(e) => setScenario({ ...scenario, tier2_capital: e.target.value })}
                                placeholder="0"
                                className="w-full px-3 py-2 bg-background border border-surface-light rounded-lg focus:outline-none focus:ring-2 focus:ring-primary text-text text-sm"
                            />
                        </div>
                    </div>
                </div>

                {/* Submit Button */}
                <button
                    type="submit"
                    disabled={loading || !query}
                    className="w-full bg-gradient-to-r from-primary to-primary-dark hover:from-primary-dark hover:to-primary text-white font-semibold py-3 px-6 rounded-lg transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-2"
                >
                    {loading ? (
                        <>
                            <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin"></div>
                            Processing...
                        </>
                    ) : (
                        <>
                            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                            </svg>
                            Generate COREP Output
                        </>
                    )}
                </button>
            </form>
        </div>
    );
}
