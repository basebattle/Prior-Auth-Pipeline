"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import {
    ShieldCheck,
    FileText,
    CheckCircle,
    XCircle,
    Download,
    AlertTriangle,
    ChevronDown,
    FileSearch,
    Stethoscope,
    ArrowRight,
    Loader2,
    ScrollText
} from "lucide-react";
import { cn } from "@/lib/utils";

export function DecisionPackage() {
    const searchParams = useSearchParams();
    const rid = searchParams.get("id");
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [deciding, setDeciding] = useState<string | null>(null);

    useEffect(() => {
        if (rid) {
            const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
            fetch(`${baseUrl}/api/requests/${rid}`)
                .then(res => res.json())
                .then(res => {
                    setData(res);
                    setLoading(false);
                })
                .catch(console.error);
        } else {
            setLoading(false);
        }
    }, [rid]);

    const handleDecision = async (status: string) => {
        setDeciding(status);
        try {
            const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
            await fetch(`${baseUrl}/api/review/${rid}`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ status })
            });
            // Refresh data
            const res = await fetch(`${baseUrl}/api/requests/${rid}`);
            setData(await res.json());
        } catch (err) {
            console.error(err);
        } finally {
            setDeciding(null);
        }
    };

    if (loading) return (
        <div className="flex flex-col items-center justify-center p-20 gap-4">
            <Loader2 className="size-10 text-blue-500 animate-spin" />
            <p className="text-neutral-500 font-medium">Downloading Multi-Agent Packet...</p>
        </div>
    );

    if (!data) return (
        <div className="text-center p-20 border border-neutral-800 rounded-3xl bg-neutral-900/50">
            <AlertTriangle className="size-10 text-yellow-500 mx-auto mb-4" />
            <h3 className="text-xl font-bold text-white">No Decision Packet Found</h3>
            <p className="text-neutral-500 mt-2">The selected PA cycle has not reached the Decision Synthesis phase.</p>
        </div>
    );

    const pkg = data.result_package || {};
    const riskColor = pkg.risk_level === 'low' ? 'text-emerald-400' : pkg.risk_level === 'medium' ? 'text-yellow-400' : 'text-red-400';

    return (
        <div className="max-w-6xl mx-auto grid lg:grid-cols-3 gap-8 animate-fade-in pb-20">
            {/* Left: Summary & Action */}
            <div className="lg:col-span-1 space-y-6">
                <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 space-y-6">
                    <div className="flex items-center gap-3">
                        <div className="size-10 bg-blue-600 rounded-xl flex items-center justify-center">
                            <ShieldCheck className="size-6 text-white" />
                        </div>
                        <div>
                            <h3 className="text-lg font-bold text-white tracking-tight">Review Verdict</h3>
                            <p className="text-[10px] text-neutral-500 font-bold uppercase tracking-widest leading-none">Checkpoint ID: {rid?.slice(0, 8)}</p>
                        </div>
                    </div>

                    <div className="space-y-4 pt-4 border-t border-neutral-800">
                        <div className="flex justify-between items-end">
                            <span className="text-xs text-neutral-500 font-bold uppercase tracking-wider">Confidence</span>
                            <span className="text-2xl font-black text-white italic">{Math.round((pkg.confidence_score || 0) * 100)}%</span>
                        </div>
                        <div className="w-full h-2 bg-neutral-950 rounded-full overflow-hidden border border-neutral-800/50">
                            <div
                                className="h-full bg-gradient-to-r from-blue-600 to-cyan-400"
                                style={{ width: `${(pkg.confidence_score || 0) * 100}%` }}
                            />
                        </div>
                        <div className="flex justify-between items-center text-xs">
                            <span className="text-neutral-500 font-medium">Risk Assessment</span>
                            <span className={cn("font-bold uppercase tracking-widest", riskColor)}>{pkg.risk_level}</span>
                        </div>
                    </div>
                </div>

                <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 space-y-4">
                    <h4 className="text-xs font-bold text-neutral-500 uppercase tracking-widest">Global Action</h4>
                    <div className="grid gap-3">
                        <button
                            onClick={() => handleDecision('approved')}
                            disabled={!!deciding || data.status === 'approved'}
                            className={cn(
                                "w-full flex items-center justify-center gap-3 py-4 rounded-xl font-bold transition-all",
                                data.status === 'approved'
                                    ? "bg-emerald-500/10 border border-emerald-500/30 text-emerald-500"
                                    : "bg-emerald-600 hover:bg-emerald-500 text-white shadow-lg shadow-emerald-900/20 active:scale-95 disabled:opacity-50"
                            )}
                        >
                            {deciding === 'approved' ? <Loader2 className="animate-spin size-4" /> : <CheckCircle className="size-5" />}
                            {data.status === 'approved' ? "Authorized" : "Confirm Approval"}
                        </button>

                        <button
                            onClick={() => handleDecision('rejected')}
                            disabled={!!deciding || data.status === 'rejected'}
                            className={cn(
                                "w-full flex items-center justify-center gap-3 py-4 rounded-xl font-bold transition-all",
                                data.status === 'rejected'
                                    ? "bg-red-500/10 border border-red-500/30 text-red-500"
                                    : "bg-neutral-950 border border-neutral-800 hover:bg-neutral-900 text-white active:scale-95 disabled:opacity-50"
                            )}
                        >
                            {deciding === 'rejected' ? <Loader2 className="animate-spin size-4" /> : <XCircle className="size-5" />}
                            {data.status === 'rejected' ? "PA Rejected" : "Deny Request"}
                        </button>
                    </div>
                </div>

                <button className="w-full flex items-center justify-between px-6 py-4 bg-neutral-900/50 border border-neutral-800 rounded-xl text-neutral-400 hover:text-white hover:bg-neutral-900 transition-all group">
                    <div className="flex items-center gap-3">
                        <Download className="size-4" />
                        <span className="text-sm font-bold">Export Case Artifacts</span>
                    </div>
                    <ChevronDown className="size-4 group-hover:translate-y-0.5 transition-transform" />
                </button>
            </div>

            {/* Right: Detailed Package */}
            <div className="lg:col-span-2 space-y-8">
                {/* Cover Sheet */}
                <Section title="Automated Cover Sheet" icon={<ScrollText />}>
                    <div className="bg-neutral-900/30 rounded-xl p-8 border border-neutral-800/50 leading-relaxed text-neutral-300 whitespace-pre-wrap font-serif italic text-lg opacity-80">
                        {pkg.cover_sheet || "Cover sheet generation in progress..."}
                    </div>
                </Section>

                {/* Necessity Argument */}
                <Section title="Clinical Necessity Argument" icon={<Stethoscope />}>
                    <div className="bg-neutral-900 rounded-xl p-8 border border-neutral-800 space-y-4">
                        <p className="text-neutral-300 leading-relaxed line-clamp-10 whitespace-pre-wrap">
                            {pkg.medical_necessity_argument || "No necessity argument provided."}
                        </p>
                        <div className="flex flex-wrap gap-2 pt-4">
                            {data.diagnosis_codes?.map((c: string) => (
                                <span key={c} className="px-2 py-1 bg-neutral-950 border border-neutral-800 rounded text-[10px] font-mono text-blue-400 font-bold uppercase tracking-tighter">{c}</span>
                            ))}
                        </div>
                    </div>
                </Section>

                {/* Checklist */}
                <Section title="Documentation Evidence Check" icon={<FileSearch />}>
                    <div className="grid gap-3">
                        {pkg.documentation_checklist?.map((item: any, i: number) => (
                            <div key={i} className="flex items-center justify-between p-4 bg-neutral-900 border border-neutral-800 rounded-xl">
                                <div className="flex items-center gap-3">
                                    {item.status === 'present'
                                        ? <CheckCircle className="size-5 text-emerald-500" />
                                        : <XCircle className="size-5 text-red-500" />
                                    }
                                    <span className="text-sm font-medium text-neutral-300">{item.item}</span>
                                </div>
                                <span className={cn(
                                    "text-[10px] font-black uppercase tracking-widest",
                                    item.status === 'present' ? "text-emerald-500" : "text-red-500"
                                )}>
                                    {item.status}
                                </span>
                            </div>
                        )) || <p className="text-neutral-500 text-sm">No checklist generated.</p>}
                    </div>
                </Section>
            </div>
        </div>
    );
}

function Section({ children, title, icon }: any) {
    return (
        <div className="space-y-4">
            <div className="flex items-center gap-3 text-neutral-400">
                <div className="size-8 rounded-lg bg-neutral-900 border border-neutral-800 flex items-center justify-center">
                    {icon && <div className="size-4">{icon}</div>}
                </div>
                <h3 className="text-sm border-neutral-400 font-black uppercase tracking-[0.2em]">{title}</h3>
            </div>
            {children}
        </div>
    );
}
