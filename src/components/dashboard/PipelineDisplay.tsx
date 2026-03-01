"use client";

import { useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import {
    CheckCircle2,
    Clock,
    AlertCircle,
    ChevronRight,
    Cpu,
    ArrowRight,
    ShieldCheck,
    Stethoscope,
    Activity,
    FileSearch,
    Zap,
    Loader2
} from "lucide-react";
import { cn } from "@/lib/utils";

const AGENTS = [
    { id: 'triage', name: 'Triage Agent', icon: Activity, desc: 'Classifying request type and urgency' },
    { id: 'validation', name: 'Clinical Validation Agent', icon: FileSearch, desc: 'Matching against Medicare NCD/LCD guidelines' },
    { id: 'npi', name: 'NPI Verification Agent', icon: ShieldCheck, desc: 'Authenticating provider credentials' },
    { id: 'necessity', name: 'Medical Necessity Agent', icon: Stethoscope, desc: 'Mapping clinical evidence from notes' },
    { id: 'risk', name: 'Denial Risk Agent', icon: Zap, desc: 'Evaluating historical approval patterns' },
    { id: 'synthesis', name: 'Decision Synthesis Agent', icon: Cpu, desc: 'Assembling clinical justification bundle' }
];

export function PipelineDisplay() {
    const searchParams = useSearchParams();
    const idFromUrl = searchParams.get("id");
    const [requestId, setRequestId] = useState<string | null>(null);
    const [data, setData] = useState<any>(null);
    const [loading, setLoading] = useState(true);
    const [progress, setProgress] = useState(0);

    useEffect(() => {
        const rid = idFromUrl || sessionStorage.getItem("last_request_id");
        setRequestId(rid);

        if (rid) {
            pollData(rid);
        } else {
            setLoading(false);
        }
    }, [idFromUrl]);

    const pollData = async (rid: string) => {
        try {
            const resp = await fetch(`http://localhost:8000/api/requests/${rid}`);
            if (resp.ok) {
                const result = await resp.json();
                setData(result);
                if (result.status === 'complete' || result.result_package) {
                    setProgress(100);
                } else {
                    // Mock progress for demo if still processing
                    const p = setInterval(() => {
                        setProgress(prev => {
                            if (prev >= 90) {
                                clearInterval(p);
                                return 90;
                            }
                            return prev + 5;
                        });
                    }, 2000);
                }
            }
        } catch (err) {
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    if (!requestId) {
        return (
            <div className="flex flex-col items-center justify-center p-20 text-center space-y-4">
                <div className="size-20 bg-neutral-900 rounded-3xl flex items-center justify-center border border-neutral-800">
                    <Activity className="size-8 text-neutral-500" />
                </div>
                <div>
                    <h3 className="text-xl font-bold text-white">No active pipeline</h3>
                    <p className="text-neutral-500 max-w-sm mx-auto mt-2">Initialize a new Prior Authorization request to see our multi-agent swarm in action.</p>
                </div>
            </div>
        );
    }

    return (
        <div className="max-w-5xl mx-auto space-y-8 animate-fade-in">
            {/* Status Banner */}
            <div className="bg-neutral-900 border border-neutral-800 rounded-3xl p-8 flex items-center justify-between shadow-2xl shadow-blue-900/10">
                <div className="space-y-1">
                    <div className="flex items-center gap-3">
                        <h2 className="text-3xl font-bold text-white tracking-tight leading-none uppercase">Analyzing PA-{requestId.slice(0, 8)}</h2>
                        {progress < 100 ? (
                            <div className="px-2 py-0.5 rounded bg-blue-500/10 text-blue-400 text-[10px] font-bold border border-blue-500/20 animate-pulse uppercase">In Progress</div>
                        ) : (
                            <div className="px-2 py-0.5 rounded bg-emerald-500/10 text-emerald-400 text-[10px] font-bold border border-emerald-500/20 uppercase">Complete</div>
                        )}
                    </div>
                    <p className="text-neutral-400 text-sm">{data?.patient_name || 'Generic Patient'} • {data?.procedure_code || 'Generic Procedure'}</p>
                </div>
                <div className="text-right hidden sm:block">
                    <p className="text-[10px] uppercase font-bold text-neutral-500 tracking-widest mb-1">Global Pipeline Status</p>
                    <p className="text-2xl font-black text-white leading-none tracking-tighter">{progress}%</p>
                </div>
            </div>

            {/* Swarm Grid */}
            <div className="grid gap-4">
                {AGENTS.map((agent, index) => {
                    const stepCompleted = progress > (index + 1) * 15 || progress === 100;
                    const stepActive = progress > index * 15 && progress <= (index + 1) * 15 && progress !== 100;
                    return (
                        <div
                            key={agent.id}
                            className={cn(
                                "relative p-6 rounded-2xl border transition-all duration-500 group",
                                stepCompleted ? "bg-neutral-900/40 border-emerald-500/30" :
                                    stepActive ? "bg-blue-600/5 border-blue-500/50 shadow-lg shadow-blue-900/10 scale-[1.02]" :
                                        "bg-neutral-950 border-neutral-900 opacity-50"
                            )}
                        >
                            <div className="flex items-center justify-between relative z-10">
                                <div className="flex items-center gap-5">
                                    <div className={cn(
                                        "size-12 rounded-xl flex items-center justify-center transition-all duration-500",
                                        stepCompleted ? "bg-emerald-500/10 text-emerald-400" :
                                            stepActive ? "bg-blue-600 text-white animate-pulse shadow-lg shadow-blue-600/20" :
                                                "bg-neutral-800 text-neutral-500"
                                    )}>
                                        <agent.icon className="size-6" />
                                    </div>
                                    <div>
                                        <h4 className={cn("font-bold", stepCompleted ? "text-neutral-200" : stepActive ? "text-white" : "text-neutral-500")}>
                                            {agent.name}
                                        </h4>
                                        <p className="text-xs text-neutral-500 mt-0.5">{agent.desc}</p>
                                    </div>
                                </div>
                                <div className="flex items-center gap-4">
                                    {stepCompleted && (
                                        <div className="flex items-center gap-1.5 text-xs font-bold text-emerald-500 uppercase">
                                            <CheckCircle2 className="size-4" />
                                            Success
                                        </div>
                                    )}
                                    {stepActive && (
                                        <Loader2 className="size-4 text-blue-500 animate-spin" />
                                    )}
                                    {!stepCompleted && !stepActive && (
                                        <Clock className="size-4 text-neutral-700" />
                                    )}
                                </div>
                            </div>

                            {/* Progress line connector */}
                            {index < AGENTS.length - 1 && (
                                <div className="absolute left-[39px] top-[68px] w-px h-6 bg-neutral-800 pointer-events-none z-0 overflow-hidden">
                                    <div className={cn(
                                        "w-full h-full bg-blue-500 transition-all duration-1000 origin-top scale-y-0",
                                        stepCompleted && "scale-y-100 bg-emerald-500"
                                    )} />
                                </div>
                            )}
                        </div>
                    )
                })}
            </div>

            {progress === 100 && (
                <button
                    onClick={() => window.location.href = `/console/review?id=${requestId}`}
                    className="w-full group py-5 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-50 text-white font-black rounded-2xl shadow-xl transition-all flex items-center justify-center gap-4 hover:scale-[1.01] active:scale-95"
                >
                    <span className="uppercase tracking-[0.2em] text-sm">Open Human Review Checkpoint</span>
                    <ArrowRight className="size-5 group-hover:translate-x-2 transition-transform" />
                </button>
            )}
        </div>
    );
}
