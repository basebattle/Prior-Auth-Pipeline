"use client";

import { Sidebar } from "./Sidebar";
import {
    Bell,
    Search,
    Menu,
    Cpu,
    Globe
} from "lucide-react";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
    return (
        <div className="flex h-screen bg-black">
            {/* Sidebar - Desktop */}
            <div className="hidden lg:flex lg:w-72 lg:flex-col">
                <Sidebar />
            </div>

            <div className="flex flex-1 flex-col overflow-hidden">
                {/* Header */}
                <header className="h-16 border-b border-neutral-800 bg-neutral-950 flex items-center justify-between px-8 shrink-0">
                    <div className="flex items-center gap-4 lg:hidden">
                        <button className="text-neutral-400">
                            <Menu className="size-6" />
                        </button>
                    </div>

                    <div className="flex-1 max-w-xl mx-auto hidden md:block">
                        <div className="relative group">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 size-4 text-neutral-500 group-focus-within:text-blue-500 transition-colors" />
                            <input
                                type="text"
                                placeholder="Search patients, protocols, or request IDs..."
                                className="w-full bg-neutral-900 border border-neutral-800 rounded-full py-2 pl-10 pr-4 text-sm text-neutral-300 focus:outline-none focus:border-blue-500 transition-all"
                            />
                        </div>
                    </div>

                    <div className="flex items-center gap-6">
                        <div className="hidden sm:flex items-center gap-3 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20">
                            <Cpu className="size-3.5 text-emerald-400" />
                            <span className="text-[10px] uppercase font-bold text-emerald-400 tracking-wider">Engine: Cloud-Sonic</span>
                        </div>

                        <button className="relative text-neutral-400 hover:text-white transition-colors">
                            <Bell className="size-5" />
                            <span className="absolute -top-1 -right-1 size-2.5 bg-blue-600 rounded-full border-2 border-neutral-950" />
                        </button>
                        <div className="size-8 rounded-lg bg-gradient-to-br from-neutral-700 to-neutral-900 border border-neutral-800 flex items-center justify-center text-xs font-bold text-neutral-400">
                            PS
                        </div>
                    </div>
                </header>

                {/* Content */}
                <main className="flex-1 overflow-y-auto p-8 bg-[url('https://www.transparenttextures.com/patterns/dark-matter.png')] bg-fixed">
                    {children}
                </main>
            </div>
        </div>
    );
}
