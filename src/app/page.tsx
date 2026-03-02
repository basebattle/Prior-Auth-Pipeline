import { InteractiveGlobe } from "@/components/ui/interactive-globe";
import { Activity, ShieldCheck, Zap, Database, Globe as GlobeIcon, ArrowRight } from "lucide-react";
import Link from "next/link";

export default function LandingPage() {
    return (
        <div className="min-h-screen bg-neutral-950 text-neutral-50 selection:bg-blue-500/30">
            {/* Background patterns */}
            <div className="fixed inset-0 overflow-hidden pointer-events-none opacity-20">
                <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] rounded-full bg-blue-600/20 blur-[120px]" />
                <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] rounded-full bg-cyan-600/20 blur-[120px]" />
            </div>

            {/* Navigation */}
            <nav className="relative z-50 border-b border-neutral-800/50 bg-neutral-950/80 backdrop-blur-md">
                <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <div className="size-8 bg-blue-600 rounded-lg flex items-center justify-center font-bold italic text-white shadow-lg shadow-blue-900/20">
                            P
                        </div>
                        <span className="font-bold tracking-tight text-lg">Priora<span className="text-blue-500 text-xl italic ml-1">Pipeline</span></span>
                    </div>
                    <div className="hidden md:flex items-center gap-8 text-sm font-medium text-neutral-400">
                        <Link href="/console/visualizer" className="hover:text-blue-400 transition-colors">Pipeline Visualizer</Link>
                        <Link href="/console/analytics" className="hover:text-blue-400 transition-colors">Analytics</Link>
                        <Link href="/console/review" className="hover:text-blue-400 transition-colors">Human Review</Link>
                    </div>
                    <Link href="/console" className="px-5 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-full text-sm font-semibold transition-all shadow-lg shadow-blue-900/40 hover:scale-105 active:scale-95">
                        Launch Console
                    </Link>
                </div>
            </nav>

            {/* Hero Section */}
            <main className="relative z-10 pt-20 pb-32 overflow-hidden">
                <div className="max-w-7xl mx-auto px-6 grid md:grid-cols-2 items-center gap-12">
                    {/* Content */}
                    <div className="flex flex-col justify-center">
                        <div className="inline-flex items-center gap-2 rounded-full border border-blue-500/30 bg-blue-500/10 px-3 py-1 text-xs font-semibold text-blue-400 mb-6 w-fit animate-fade-in">
                            <span className="size-2 rounded-full bg-blue-400 animate-pulse" />
                            Multi-Agentic Prior-Auth Network Active
                        </div>

                        <h1 className="text-4xl md:text-5xl lg:text-7xl font-bold tracking-tight leading-[1.1] mb-6">
                            Agentic Healthcare
                            <br />
                            <span className="bg-gradient-to-r from-blue-400 via-cyan-300 to-indigo-400 bg-clip-text text-transparent">
                                Prior-Auth Pipeline
                            </span>
                        </h1>

                        <p className="text-lg text-neutral-400 max-w-lg leading-relaxed mb-10">
                            Automate medical necessity reviews with 99.9% protocol compliance.
                            Our multi-agent swarm processes clinical documentation at the edge,
                            reducing average PA turnaround from 7 days to 5 seconds.
                        </p>

                        <div className="flex flex-wrap items-center gap-4 mb-12">
                            <Link href="/console/new-request" className="px-8 py-4 bg-white text-black hover:bg-neutral-200 font-bold rounded-xl transition-all flex items-center gap-2 group">
                                New PA Request <ArrowRight className="size-5 group-hover:translate-x-1 transition-transform" />
                            </Link>
                            <Link href="/console/manual" className="px-8 py-4 bg-neutral-900 border border-neutral-800 hover:bg-neutral-800 text-white font-bold rounded-xl transition-all">
                                View Documentation
                            </Link>
                        </div>

                        <div className="grid grid-cols-3 gap-8 py-8 border-t border-neutral-800/50">
                            <div>
                                <p className="text-3xl font-bold text-white tracking-tight">150+</p>
                                <p className="text-xs font-medium text-neutral-500 uppercase tracking-wider mt-1">Medical Protocols</p>
                            </div>
                            <div>
                                <p className="text-3xl font-bold text-white tracking-tight">&lt;5s</p>
                                <p className="text-xs font-medium text-neutral-500 uppercase tracking-wider mt-1">Avg Latency</p>
                            </div>
                            <div>
                                <p className="text-3xl font-bold text-white tracking-tight">92%</p>
                                <p className="text-xs font-medium text-neutral-500 uppercase tracking-wider mt-1">Manual Savings</p>
                            </div>
                        </div>
                    </div>

                    {/* Right — Interactive Globe */}
                    <div className="relative flex items-center justify-center min-h-[500px] md:min-h-[600px] pointer-events-auto">
                        {/* Radial backlights */}
                        <div className="absolute inset-0 bg-blue-500/5 rounded-full blur-[100px] scale-150 rotate-12" />
                        <div className="absolute inset-0 bg-cyan-400/5 rounded-full blur-[120px] scale-125 -rotate-12" />

                        <InteractiveGlobe
                            size={580}
                            markerColor="rgba(56, 189, 248, 1)"
                            dotColor="rgba(56, 189, 248, ALPHA)"
                            arcColor="rgba(56, 189, 248, 0.4)"
                        />
                    </div>
                </div>
            </main>

            {/* Feature Grid */}
            <section className="relative z-10 py-24 bg-neutral-900/30">
                <div className="max-w-7xl mx-auto px-6">
                    <div className="grid md:grid-cols-2 lg:grid-cols-4 gap-8">
                        <FeatureCard
                            icon={<ShieldCheck className="text-emerald-400" />}
                            title="Protocol Compliance"
                            description="Real-time verification against Medicare NCD/LCD and commercial medical policies."
                        />
                        <FeatureCard
                            icon={<Zap className="text-yellow-400" />}
                            title="Sub-5s Decisions"
                            description="Concurrent agent execution ensures decisions are ready before the provider clicks submit."
                        />
                        <FeatureCard
                            icon={<Activity className="text-blue-400" />}
                            title="Clinical Swarm"
                            description="Specialized LLM agents for NPI verification, medical necessity, and risk assessment."
                        />
                        <FeatureCard
                            icon={<Database className="text-purple-400" />}
                            title="Semantic Evidence"
                            description="Extracts clinical evidence from unstructured EMR notes with citation mapping."
                        />
                    </div>
                </div>
            </section>
        </div>
    );
}

function FeatureCard({ icon, title, description }: { icon: React.ReactNode, title: string, description: string }) {
    return (
        <div className="p-8 rounded-2xl bg-neutral-900/50 border border-neutral-800 hover:border-neutral-700 transition-all hover:-translate-y-1 group">
            <div className="size-12 rounded-xl bg-neutral-800 flex items-center justify-center mb-6 group-hover:scale-110 transition-transform">
                {icon}
            </div>
            <h3 className="text-xl font-bold mb-3 text-neutral-100">{title}</h3>
            <p className="text-neutral-400 text-sm leading-relaxed">{description}</p>
        </div>
    );
}
