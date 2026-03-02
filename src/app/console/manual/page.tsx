import { HelpCircle, BookOpen, MessageSquare, Info } from "lucide-react";

export default function ManualPage() {
    return (
        <div className="max-w-4xl mx-auto space-y-8 animate-fade-in pb-12">
            <div className="flex items-center gap-4 border-b border-neutral-800 pb-6">
                <div className="size-12 bg-blue-600/10 rounded-xl flex items-center justify-center text-blue-500">
                    <HelpCircle className="size-6" />
                </div>
                <div>
                    <h1 className="text-3xl font-bold text-white">User Manual</h1>
                    <p className="text-neutral-400">A guide to automating healthcare approvals with Priora-Pipeline</p>
                </div>
            </div>

            <section className="space-y-6">
                <div className="bg-neutral-900/50 border border-neutral-800 rounded-2xl p-8 space-y-6">
                    <div className="flex items-center gap-3 text-blue-400">
                        <BookOpen className="size-5" />
                        <h2 className="text-xl font-bold">1. Getting Started</h2>
                    </div>
                    <p className="text-neutral-300 leading-relaxed">
                        Welcome to the Prior Auth Pipeline. This system is designed to help clinical staff and administrative teams process Prior Authorization (PA) requests faster and with higher accuracy using AI technology. Navigate through the sidebar on the left.
                    </p>
                    <div className="grid grid-cols-3 gap-4">
                        <div className="bg-neutral-950 p-4 rounded-xl border border-neutral-800">
                            <span className="text-blue-500 font-bold block mb-1 text-xs">01</span>
                            <span className="text-white font-semibold text-sm">Submit</span>
                            <span className="text-[10px] text-neutral-500 block mt-1">Start a new request</span>
                        </div>
                        <div className="bg-neutral-950 p-4 rounded-xl border border-neutral-800">
                            <span className="text-blue-500 font-bold block mb-1 text-xs">02</span>
                            <span className="text-white font-semibold text-sm">Monitor</span>
                            <span className="text-[10px] text-neutral-500 block mt-1">Real-time AI review</span>
                        </div>
                        <div className="bg-neutral-950 p-4 rounded-xl border border-neutral-800">
                            <span className="text-blue-500 font-bold block mb-1 text-xs">03</span>
                            <span className="text-white font-semibold text-sm">Review</span>
                            <span className="text-[10px] text-neutral-500 block mt-1">Final decision package</span>
                        </div>
                    </div>
                </div>

                <div className="grid md:grid-cols-2 gap-6">
                    <div className="bg-neutral-900/50 border border-neutral-800 rounded-2xl p-6 space-y-4">
                        <h3 className="font-bold text-white flex items-center gap-2">
                            <Info className="size-4 text-blue-400" />
                            Submission Methods
                        </h3>
                        <ul className="space-y-3 text-sm text-neutral-400">
                            <li className="flex gap-3">
                                <span className="text-blue-500 font-bold">•</span>
                                <span><strong className="text-neutral-200">Manual Entry:</strong> Type clinical notes directly.</span>
                            </li>
                            <li className="flex gap-3">
                                <span className="text-blue-500 font-bold">•</span>
                                <span><strong className="text-neutral-200">OCR Upload:</strong> Upload records; AI extracts facts.</span>
                            </li>
                            <li className="flex gap-3">
                                <span className="text-blue-500 font-bold">•</span>
                                <span><strong className="text-neutral-200">Voice-to-PA:</strong> Transcribe summaries directly.</span>
                            </li>
                        </ul>
                    </div>
                    <div className="bg-neutral-900/50 border border-neutral-800 rounded-2xl p-6 space-y-4">
                        <h3 className="font-bold text-white flex items-center gap-2">
                            <MessageSquare className="size-4 text-blue-400" />
                            Clinical Agents
                        </h3>
                        <ul className="space-y-3 text-sm text-neutral-400">
                            <li className="flex gap-3">
                                <span className="text-blue-500 font-bold">•</span>
                                <span><strong className="text-neutral-200">Clinical Validation:</strong> Policy checks.</span>
                            </li>
                            <li className="flex gap-3">
                                <span className="text-blue-500 font-bold">•</span>
                                <span><strong className="text-neutral-200">Medical Necessity:</strong> Evidence building.</span>
                            </li>
                            <li className="flex gap-3">
                                <span className="text-blue-500 font-bold">•</span>
                                <span><strong className="text-neutral-200">Denial Risk:</strong> Predict outcome and fix.</span>
                            </li>
                        </ul>
                    </div>
                </div>

                <div className="bg-blue-600/10 border border-blue-500/20 rounded-2xl p-6">
                    <h3 className="font-bold text-blue-400 mb-2">🆘 Support</h3>
                    <p className="text-sm text-neutral-400">
                        For technical issues, contact the IT department. This system uses synthetic data for demonstration purposes in connected environments.
                    </p>
                </div>
            </section>
        </div>
    );
}
