export default function AnalyticsPage() {
    return (
        <div className="space-y-6">
            <h1 className="text-2xl font-bold text-white">Analytics Dashboard</h1>
            <div className="bg-neutral-900/50 border border-neutral-800 rounded-2xl p-12 flex flex-col items-center justify-center text-center">
                <div className="size-16 bg-blue-600/10 rounded-full flex items-center justify-center mb-6">
                    <div className="size-8 bg-blue-600 rounded-lg flex items-center justify-center font-bold italic text-white">P</div>
                </div>
                <h3 className="text-xl font-bold text-white mb-2">Analytics Engine Coming Soon</h3>
                <p className="text-neutral-400 max-w-sm">
                    We are currently calibrating the multi-agent synthesis engine to provide real-time performance metrics and protocol compliance trends.
                </p>
            </div>
        </div>
    );
}
