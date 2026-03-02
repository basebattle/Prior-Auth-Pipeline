"use client";

import { useState, useEffect } from "react";
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
    PieChart, Pie, Cell, LineChart, Line, AreaChart, Area
} from "recharts";
import { Activity, CheckCircle, XCircle, Clock, Zap, Target, TrendingUp } from "lucide-react";

const APPROVAL_DATA = [
    { name: "Mon", approvals: 45, denials: 12 },
    { name: "Tue", approvals: 52, denials: 8 },
    { name: "Wed", approvals: 48, denials: 15 },
    { name: "Thu", approvals: 61, denials: 10 },
    { name: "Fri", approvals: 55, denials: 20 },
    { name: "Sat", approvals: 30, denials: 5 },
    { name: "Sun", approvals: 25, denials: 3 },
];

const PIE_DATA = [
    { name: "Approved", value: 72 },
    { name: "Denied", value: 18 },
    { name: "Appealed", value: 10 },
];

const COLORS = ["#3b82f6", "#ef4444", "#8b5cf6"];

const LATENCY_DATA = [
    { time: "09:00", ms: 4500 },
    { time: "10:00", ms: 5200 },
    { time: "11:00", ms: 4800 },
    { time: "12:00", ms: 8100 },
    { time: "13:00", ms: 3900 },
    { time: "14:00", ms: 4200 },
    { time: "15:00", ms: 5600 },
];

export default function AnalyticsPage() {
    const [isMounted, setIsMounted] = useState(false);

    useEffect(() => {
        setIsMounted(true);
    }, []);

    if (!isMounted) return null;

    return (
        <div className="space-y-8 pb-12 animate-fade-in">
            <header className="flex flex-col gap-2">
                <h1 className="text-3xl font-bold text-white tracking-tight">Intelligence Dashboard</h1>
                <p className="text-neutral-500">Real-time performance metrics and protocol compliance trends.</p>
            </header>

            {/* Stats Overview */}
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <StatCard
                    label="Total Requests"
                    value="1,429"
                    trend="+12%"
                    icon={Activity}
                    color="blue"
                />
                <StatCard
                    label="Avg. Turnaround"
                    value="5.2s"
                    trend="-85%"
                    icon={Zap}
                    color="emerald"
                />
                <StatCard
                    label="Auto-Approval Rate"
                    value="78.4%"
                    trend="+2.1%"
                    icon={CheckCircle}
                    color="indigo"
                />
                <StatCard
                    label="Protocol Fidelity"
                    value="99.9%"
                    trend="Ideal"
                    icon={Target}
                    color="purple"
                />
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                {/* Main Volume Chart */}
                <div className="lg:col-span-2 bg-neutral-900/50 border border-neutral-800 rounded-3xl p-6">
                    <h3 className="text-lg font-bold text-white mb-6">Approval Volume vs Denials</h3>
                    <div className="h-80 w-full">
                        <ResponsiveContainer width="100%" height="100%">
                            <BarChart data={APPROVAL_DATA}>
                                <CartesianGrid strokeDasharray="3 3" stroke="#262626" vertical={false} />
                                <XAxis dataKey="name" axisLine={false} tickLine={false} tick={{ fill: '#737373', fontSize: 12 }} />
                                <YAxis axisLine={false} tickLine={false} tick={{ fill: '#737373', fontSize: 12 }} />
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#0a0a0a', border: '1px solid #262626', borderRadius: '12px' }}
                                    itemStyle={{ fontSize: '12px' }}
                                />
                                <Bar dataKey="approvals" fill="#3b82f6" radius={[4, 4, 0, 0]} barSize={30} />
                                <Bar dataKey="denials" fill="#ef4444" radius={[4, 4, 0, 0]} barSize={30} />
                            </BarChart>
                        </ResponsiveContainer>
                    </div>
                </div>

                {/* Outcome Distribution */}
                <div className="bg-neutral-900/50 border border-neutral-800 rounded-3xl p-6">
                    <h3 className="text-lg font-bold text-white mb-6">Outcome Distribution</h3>
                    <div className="h-64 w-full relative">
                        <ResponsiveContainer width="100%" height="100%">
                            <PieChart>
                                <Pie
                                    data={PIE_DATA}
                                    innerRadius={60}
                                    outerRadius={80}
                                    paddingAngle={5}
                                    dataKey="value"
                                >
                                    {PIE_DATA.map((entry, index) => (
                                        <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                                    ))}
                                </Pie>
                                <Tooltip
                                    contentStyle={{ backgroundColor: '#0a0a0a', border: '1px solid #262626', borderRadius: '12px' }}
                                />
                            </PieChart>
                        </ResponsiveContainer>
                        <div className="absolute inset-0 flex flex-col items-center justify-center pointer-events-none">
                            <span className="text-2xl font-black text-white">72%</span>
                            <span className="text-[10px] text-neutral-500 uppercase font-bold">Approved</span>
                        </div>
                    </div>
                    <div className="space-y-3 mt-4">
                        {PIE_DATA.map((item, i) => (
                            <div key={item.name} className="flex items-center justify-between text-sm">
                                <div className="flex items-center gap-2 text-neutral-400">
                                    <div className="size-2 rounded-full" style={{ backgroundColor: COLORS[i] }} />
                                    {item.name}
                                </div>
                                <span className="font-bold text-white">{item.value}%</span>
                            </div>
                        ))}
                    </div>
                </div>
            </div>

            {/* Latency History */}
            <div className="bg-neutral-900/50 border border-neutral-800 rounded-3xl p-6">
                <div className="flex items-center justify-between mb-8">
                    <div>
                        <h3 className="text-lg font-bold text-white">Swarm Latency Analysis</h3>
                        <p className="text-xs text-neutral-500">Average processing time across multi-agent nodes (ms)</p>
                    </div>
                    <div className="flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-bold">
                        <TrendingDown className="size-3" />
                        Target: 5000ms
                    </div>
                </div>
                <div className="h-64 w-full">
                    <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={LATENCY_DATA}>
                            <defs>
                                <linearGradient id="colorMs" x1="0" y1="0" x2="0" y2="1">
                                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                                </linearGradient>
                            </defs>
                            <CartesianGrid strokeDasharray="3 3" stroke="#262626" vertical={false} />
                            <XAxis dataKey="time" axisLine={false} tickLine={false} tick={{ fill: '#737373', fontSize: 10 }} />
                            <YAxis axisLine={false} tickLine={false} hide />
                            <Tooltip
                                contentStyle={{ backgroundColor: '#0a0a0a', border: '1px solid #262626', borderRadius: '12px' }}
                            />
                            <Area type="monotone" dataKey="ms" stroke="#3b82f6" fillOpacity={1} fill="url(#colorMs)" strokeWidth={3} />
                        </AreaChart>
                    </ResponsiveContainer>
                </div>
            </div>
        </div>
    );
}

function StatCard({ label, value, trend, icon: Icon, color }: any) {
    const colorClasses: any = {
        blue: "bg-blue-500/10 text-blue-400 border-blue-500/20",
        emerald: "bg-emerald-500/10 text-emerald-400 border-emerald-500/20",
        indigo: "bg-indigo-500/10 text-indigo-400 border-indigo-500/20",
        purple: "bg-purple-500/10 text-purple-400 border-purple-500/20",
    }

    return (
        <div className="bg-neutral-900/40 border border-neutral-800 rounded-2xl p-6 transition-all hover:border-neutral-700">
            <div className="flex items-start justify-between">
                <div className={cn("p-2 rounded-lg border", colorClasses[color])}>
                    <Icon className="size-5" />
                </div>
                <div className={cn(
                    "text-xs font-bold px-2 py-0.5 rounded-full",
                    trend.startsWith('+') ? "text-emerald-500 bg-emerald-500/10" :
                        trend.startsWith('-') ? "text-blue-500 bg-blue-500/10" : "text-neutral-400 bg-neutral-400/10"
                )}>
                    {trend}
                </div>
            </div>
            <div className="mt-4">
                <h4 className="text-3xl font-black text-white tracking-tight">{value}</h4>
                <p className="text-xs font-bold text-neutral-500 uppercase tracking-widest mt-1">{label}</p>
            </div>
        </div>
    );
}

function cn(...inputs: any[]) {
    return inputs.filter(Boolean).join(" ");
}
