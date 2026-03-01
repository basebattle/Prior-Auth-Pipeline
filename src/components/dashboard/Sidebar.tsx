"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";
import {
    PlusCircle,
    Activity,
    History,
    ShieldCheck,
    BarChart3,
    Layers,
    Settings,
    HelpCircle,
    FlaskConical
} from "lucide-react";

const navigation = [
    { name: 'New Request', href: '/console/new-request', icon: PlusCircle },
    { name: 'Pipeline Visualizer', href: '/console/visualizer', icon: Activity },
    { name: 'Human Review', href: '/console/review', icon: ShieldCheck },
    { name: 'History', href: '/console/history', icon: History },
    { name: 'Analytics', href: '/console/analytics', icon: BarChart3 },
    { name: 'Batch Processing', href: '/console/batch', icon: Layers },
];

const secondaryNavigation = [
    { name: 'User Manual', href: '/console/manual', icon: HelpCircle },
    { name: 'Settings', href: '/console/settings', icon: Settings },
];

export function Sidebar() {
    const pathname = usePathname();

    return (
        <div className="flex grow flex-col gap-y-5 overflow-y-auto bg-neutral-950 border-r border-neutral-800 px-6 pb-4">
            <div className="flex h-16 shrink-0 items-center gap-2">
                <div className="size-8 bg-blue-600 rounded-lg flex items-center justify-center font-bold italic text-white">
                    P
                </div>
                <span className="font-bold tracking-tight text-white">Priora<span className="text-blue-500 ml-1">Console</span></span>
            </div>
            <nav className="flex flex-1 flex-col">
                <ul role="list" className="flex flex-1 flex-col gap-y-7">
                    <li>
                        <ul role="list" className="-mx-2 space-y-1">
                            {navigation.map((item) => (
                                <li key={item.name}>
                                    <Link
                                        href={item.href}
                                        className={cn(
                                            pathname === item.href
                                                ? 'bg-neutral-900 text-white'
                                                : 'text-neutral-400 hover:text-white hover:bg-neutral-900',
                                            'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold transition-colors'
                                        )}
                                    >
                                        <item.icon
                                            className={cn(
                                                pathname === item.href ? 'text-blue-500' : 'text-neutral-400 group-hover:text-blue-400',
                                                'h-6 w-6 shrink-0 transition-colors'
                                            )}
                                            aria-hidden="true"
                                        />
                                        {item.name}
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    </li>

                    <li className="mt-auto">
                        <ul role="list" className="-mx-2 space-y-1">
                            {secondaryNavigation.map((item) => (
                                <li key={item.name}>
                                    <Link
                                        href={item.href}
                                        className={cn(
                                            pathname === item.href
                                                ? 'bg-neutral-900 text-white'
                                                : 'text-neutral-400 hover:text-white hover:bg-neutral-900',
                                            'group flex gap-x-3 rounded-md p-2 text-sm leading-6 font-semibold transition-colors'
                                        )}
                                    >
                                        <item.icon
                                            className={cn(
                                                pathname === item.href ? 'text-blue-500' : 'text-neutral-400 group-hover:text-blue-400',
                                                'h-6 w-6 shrink-0 transition-colors'
                                            )}
                                            aria-hidden="true"
                                        />
                                        {item.name}
                                    </Link>
                                </li>
                            ))}
                        </ul>
                    </li>

                    <div className="rounded-xl bg-blue-600/10 border border-blue-500/20 p-4">
                        <div className="flex items-center gap-2 text-blue-400 mb-2">
                            <FlaskConical className="size-4" />
                            <span className="text-xs font-bold uppercase tracking-wider">Demo Active</span>
                        </div>
                        <p className="text-[10px] text-neutral-400 leading-relaxed">
                            Connected to Local Pipeline Engine (v2.1.0). AI synthesis enabled.
                        </p>
                    </div>
                </ul>
            </nav>
        </div>
    );
}
