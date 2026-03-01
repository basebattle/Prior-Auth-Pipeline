"use client";

import { useEffect, useState } from "react";
import { format } from "date-fns";
import {
    Activity,
    ExternalLink,
    ShieldCheck,
    MoreHorizontal,
    Clock,
    CheckCircle2,
    XCircle,
    Search,
    Filter,
    Download
} from "lucide-react";
import { cn } from "@/lib/utils";
import Link from "next/link";

export function HistoryTable() {
    const [requests, setRequests] = useState<any[]>([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
        fetch(`${baseUrl}/api/requests`)
            .then(res => res.json())
            .then(data => {
                setRequests(data);
                setLoading(false);
            })
            .catch(console.error);
    }, []);

    return (
        <div className="space-y-6 animate-fade-in">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
                <div>
                    <h2 className="text-2xl font-bold text-white">PA Request Vault</h2>
                    <p className="text-neutral-500 text-sm mt-1">Audit log of all agentic decision cycles</p>
                </div>
                <div className="flex items-center gap-3">
                    <div className="relative group">
                        <Search className="absolute left-3 top-1/2 -translate-y-1/2 size-4 text-neutral-500 group-focus-within:text-blue-500 transition-colors" />
                        <input
                            type="text"
                            placeholder="Filter records..."
                            className="bg-neutral-900 border border-neutral-800 rounded-lg py-2 pl-10 pr-4 text-sm text-neutral-300 focus:outline-none focus:border-blue-400 transition-all w-full md:w-64"
                        />
                    </div>
                    <button className="p-2 bg-neutral-900 border border-neutral-800 rounded-lg text-neutral-400 hover:text-white transition-colors">
                        <Filter className="size-5" />
                    </button>
                    <button className="p-2 bg-neutral-900 border border-neutral-800 rounded-lg text-neutral-400 hover:text-white transition-colors">
                        <Download className="size-5" />
                    </button>
                </div>
            </div>

            <div className="overflow-hidden bg-neutral-950 border border-neutral-800 rounded-2xl">
                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead className="bg-neutral-900/50 border-b border-neutral-800">
                            <tr>
                                <th className="px-6 py-4 text-xs font-bold text-neutral-500 uppercase tracking-wider">Patient & ID</th>
                                <th className="px-6 py-4 text-xs font-bold text-neutral-500 uppercase tracking-wider">Payer / Procedure</th>
                                <th className="px-6 py-4 text-xs font-bold text-neutral-500 uppercase tracking-wider">Status</th>
                                <th className="px-6 py-4 text-xs font-bold text-neutral-500 uppercase tracking-wider">Confidence</th>
                                <th className="px-6 py-4 text-xs font-bold text-neutral-500 uppercase tracking-wider">Date</th>
                                <th className="px-6 py-4 text-xs font-bold text-neutral-500 uppercase tracking-wider text-right">Action</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-neutral-900">
                            {loading ? (
                                [1, 2, 3].map(i => <SkeletonRow key={i} />)
                            ) : requests.length === 0 ? (
                                <tr>
                                    <td colSpan={6} className="px-6 py-20 text-center text-neutral-500 text-sm italic">
                                        No records found. Submit a request to populate history.
                                    </td>
                                </tr>
                            ) : (
                                requests.map((req) => (
                                    <tr key={req.id} className="hover:bg-neutral-900/30 transition-colors group">
                                        <td className="px-6 py-4">
                                            <div className="flex flex-col">
                                                <span className="font-bold text-neutral-200 group-hover:text-blue-400 transition-colors">{req.patient_name}</span>
                                                <span className="text-[10px] font-mono text-neutral-600 tracking-tighter uppercase">{req.id.slice(0, 13)}</span>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <div className="flex flex-col">
                                                <span className="text-sm text-neutral-300 font-medium">{req.payer_name}</span>
                                                <span className="text-xs text-neutral-500 italic">{req.procedure_code}</span>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4">
                                            <StatusBadge status={req.status} />
                                        </td>
                                        <td className="px-6 py-4">
                                            <div className="flex items-center gap-2">
                                                <div className="w-12 h-1 bg-neutral-800 rounded-full overflow-hidden">
                                                    <div
                                                        className="h-full bg-blue-500"
                                                        style={{ width: `${(req.confidence_score || 0.85) * 100}%` }}
                                                    />
                                                </div>
                                                <span className="text-xs font-bold text-neutral-400">
                                                    {Math.round((req.confidence_score || 0.85) * 100)}%
                                                </span>
                                            </div>
                                        </td>
                                        <td className="px-6 py-4 text-xs text-neutral-500 tabular-nums">
                                            {format(new Date(req.created_at), 'MMM dd, HH:mm')}
                                        </td>
                                        <td className="px-6 py-4 text-right">
                                            <div className="flex items-center justify-end gap-2">
                                                <Link
                                                    href={`/console/visualizer?id=${req.id}`}
                                                    className="p-1.5 rounded-md hover:bg-blue-600/10 hover:text-blue-400 text-neutral-600 transition-all"
                                                >
                                                    <Activity className="size-4" />
                                                </Link>
                                                <Link
                                                    href={`/console/review?id=${req.id}`}
                                                    className="p-1.5 rounded-md hover:bg-emerald-600/10 hover:text-emerald-400 text-neutral-600 transition-all"
                                                >
                                                    <ShieldCheck className="size-4" />
                                                </Link>
                                            </div>
                                        </td>
                                    </tr>
                                ))
                            )}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    );
}

function StatusBadge({ status }: { status: string }) {
    const config: any = {
        complete: { icon: CheckCircle2, class: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20", label: "Final" },
        approved: { icon: CheckCircle2, class: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20", label: "Approved" },
        rejected: { icon: XCircle, class: "bg-red-500/10 text-red-400 border-red-500/20", label: "Denied" },
        processing: { icon: Clock, class: "bg-blue-500/10 text-blue-400 border-blue-500/20 animate-pulse", label: "Running" },
        pending: { icon: Clock, class: "bg-neutral-800 text-neutral-500 border-neutral-700", label: "Pending" }
    };

    const item = config[status] || config.pending;
    return (
        <div className={cn("inline-flex items-center gap-1.5 px-2 py-1 rounded-md border text-[10px] font-black uppercase tracking-wider", item.class)}>
            <item.icon className="size-3" />
            {item.label}
        </div>
    );
}

function SkeletonRow() {
    return (
        <tr className="animate-pulse">
            {[1, 2, 3, 4, 5, 6].map(i => (
                <td key={i} className="px-6 py-6">
                    <div className="h-2 bg-neutral-900 rounded-full w-2/3" />
                </td>
            ))}
        </tr>
    );
}
