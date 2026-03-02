export default function BatchProcessingPage() {
    return (
        <div className="space-y-6">
            <h1 className="text-2xl font-bold text-white">Batch Processing</h1>
            <div className="bg-neutral-900/50 border border-neutral-800 rounded-2xl p-12 flex flex-col items-center justify-center text-center">
                <h3 className="text-xl font-bold text-white mb-2">Concurrent Pipeline Optimization</h3>
                <p className="text-neutral-400 max-w-sm">
                    Large-scale clinical documentation batch processing is currently in beta. Reach out to your administrator to enable concurrent swarm execution for your organization.
                </p>
            </div>
        </div>
    );
}
