import { useState } from "react";
import { Sidebar } from "./Sidebar";
import {
    Bell,
    Search,
    Menu,
    Cpu,
    X
} from "lucide-react";
import { cn } from "@/lib/utils";

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
    const [isSidebarOpen, setIsSidebarOpen] = useState(false);

    return (
        <div className="flex h-screen bg-black overflow-hidden selection:bg-blue-500/30">
            {/* Sidebar - Desktop */}
            <div className="hidden lg:flex lg:w-72 lg:flex-col">
                <Sidebar />
            </div>

            {/* Mobile Sidebar Overlay */}
            <div
                className={cn(
                    "fixed inset-0 bg-black/60 backdrop-blur-sm z-40 transition-opacity lg:hidden",
                    isSidebarOpen ? "opacity-100 pointer-events-auto" : "opacity-0 pointer-events-none"
                )}
                onClick={() => setIsSidebarOpen(false)}
            />

            {/* Mobile Sidebar Panel */}
            <div className={cn(
                "fixed inset-y-0 left-0 w-72 bg-black z-50 transform transition-transform duration-300 lg:hidden",
                isSidebarOpen ? "translate-x-0" : "-translate-x-full"
            )}>
                <div className="flex justify-end p-4">
                    <button
                        onClick={() => setIsSidebarOpen(false)}
                        className="p-2 text-neutral-400 hover:text-white"
                        aria-label="Close sidebar"
                    >
                        <X className="size-6" />
                    </button>
                </div>
                <Sidebar />
            </div>

            <div className="flex flex-1 flex-col overflow-hidden">
                {/* Header */}
                <header className="h-16 border-b border-neutral-800 bg-neutral-950 flex items-center justify-between px-4 sm:px-8 shrink-0">
                    <div className="flex items-center gap-4 lg:hidden">
                        <button
                            onClick={() => setIsSidebarOpen(true)}
                            className="p-2 -ml-2 text-neutral-400 hover:text-white transition-colors"
                            aria-label="Open sidebar"
                        >
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
                                aria-label="Search dashboard"
                            />
                        </div>
                    </div>

                    <div className="flex items-center gap-4 sm:gap-6">
                        <div className="hidden sm:flex items-center gap-3 px-3 py-1.5 rounded-full bg-emerald-500/10 border border-emerald-500/20">
                            <Cpu className="size-3.5 text-emerald-400" />
                            <span className="text-[10px] uppercase font-bold text-emerald-400 tracking-wider">Engine: Cloud-Sonic</span>
                        </div>

                        <button
                            className="relative p-2 text-neutral-400 hover:text-white transition-colors"
                            aria-label="View notifications"
                        >
                            <Bell className="size-5" />
                            <span className="absolute top-1.5 right-1.5 size-2.5 bg-blue-600 rounded-full border-2 border-neutral-950" />
                        </button>
                        <div className="size-8 rounded-lg bg-gradient-to-br from-neutral-700 to-neutral-900 border border-neutral-800 flex items-center justify-center text-xs font-bold text-neutral-400 shrink-0">
                            PS
                        </div>
                    </div>
                </header>

                {/* Content */}
                <main className="flex-1 overflow-y-auto p-4 sm:p-8 bg-[url('https://www.transparenttextures.com/patterns/dark-matter.png')] bg-fixed">
                    {children}
                </main>
            </div>
        </div>
    );
}
