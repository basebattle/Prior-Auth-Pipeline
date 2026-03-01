"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import {
    Dices,
    Send,
    User,
    FileText,
    Stethoscope,
    Clock,
    Mic,
    Upload,
    Keyboard,
    CheckCircle2,
    AlertCircle,
    Loader2
} from "lucide-react";
import { cn } from "@/lib/utils";

// Mock payers for dropdown
const PAYERS = ["UnitedHealthcare", "Aetna", "BCBS", "Cigna", "Humana", "Medicare", "Medicaid"];

export function RequestForm() {
    const router = useRouter();
    const [loading, setLoading] = useState(false);
    const [randomizing, setRandomizing] = useState(false);
    const [activeTab, setActiveTab] = useState('manual');

    const [formData, setFormData] = useState({
        patient_id: "",
        patient_name: "",
        patient_dob: "",
        payer_name: "UnitedHealthcare",
        procedure_code: "",
        diagnosis_codes: "",
        requesting_provider_npi: "",
        clinical_notes: "",
        urgency: "standard"
    });

    const loadRandomData = async () => {
        setRandomizing(true);
        try {
            const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
            const resp = await fetch(`${baseUrl}/api/scenarios?count=1`);
            const data = await resp.json();
            const scenario = data[0];

            setFormData({
                patient_id: scenario.patient_id,
                patient_name: scenario.patient_name,
                patient_dob: scenario.patient_dob,
                payer_name: scenario.payer_name,
                procedure_code: scenario.procedure_code,
                diagnosis_codes: scenario.diagnosis_codes.join(", "),
                requesting_provider_npi: scenario.requesting_provider_npi,
                clinical_notes: scenario.clinical_notes,
                urgency: "standard"
            });
        } catch (err) {
            console.error("Failed to fetch scenario", err);
        } finally {
            setRandomizing(false);
        }
    };

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        try {
            const payload = {
                ...formData,
                diagnosis_codes: formData.diagnosis_codes.split(",").map(s => s.trim()).filter(Boolean)
            };

            const baseUrl = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
            const resp = await fetch(`${baseUrl}/api/submit`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(payload)
            });

            if (!resp.ok) throw new Error("Submission failed");

            const data = await resp.json();
            // Store current ID in session storage for visualizer
            sessionStorage.setItem("last_request_id", data.request_id);

            router.push(`/console/visualizer?id=${data.request_id}`);
        } catch (err) {
            alert("Pipeline Submission Error. Ensure backend is running.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto space-y-6 animate-fade-in">
            <div className="flex items-center justify-between">
                <div>
                    <h2 className="text-2xl font-bold text-white">Create New Authorization</h2>
                    <p className="text-neutral-400 text-sm mt-1">Initiate a multi-agentic medical necessity review</p>
                </div>
                <button
                    onClick={loadRandomData}
                    disabled={randomizing}
                    className="flex items-center gap-2 px-4 py-2 bg-neutral-800 hover:bg-neutral-700 text-white rounded-lg text-sm font-semibold transition-all border border-neutral-700 active:scale-95 disabled:opacity-50"
                >
                    {randomizing ? <Loader2 className="size-4 animate-spin" /> : <Dices className="size-4" />}
                    Load Randomized Case
                </button>
            </div>

            <form onSubmit={handleSubmit} className="space-y-6">
                <div className="grid md:grid-cols-2 gap-6">
                    {/* Patient Info Card */}
                    <div className="bg-neutral-900/50 border border-neutral-800 rounded-2xl p-6 space-y-4">
                        <div className="flex items-center gap-2 text-blue-400 mb-2">
                            <User className="size-4" />
                            <span className="text-xs font-bold uppercase tracking-wider">Patient Demographics</span>
                        </div>

                        <div className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <InputGroup label="Patient ID" value={formData.patient_id} onChange={(v: string) => setFormData({ ...formData, patient_id: v })} placeholder="e.g. P1001" />
                                <InputGroup label="DOB" value={formData.patient_dob} onChange={(v: string) => setFormData({ ...formData, patient_dob: v })} placeholder="YYYY-MM-DD" />
                            </div>
                            <InputGroup label="Full Name" value={formData.patient_name} onChange={(v: string) => setFormData({ ...formData, patient_name: v })} placeholder="e.g. John Doe" />
                        </div>
                    </div>

                    {/* Procedure Info Card */}
                    <div className="bg-neutral-900/50 border border-neutral-800 rounded-2xl p-6 space-y-4">
                        <div className="flex items-center gap-2 text-indigo-400 mb-2">
                            <Stethoscope className="size-4" />
                            <span className="text-xs font-bold uppercase tracking-wider">Clinical Submission</span>
                        </div>

                        <div className="space-y-4">
                            <div className="grid grid-cols-2 gap-4">
                                <InputGroup label="Procedure Code" value={formData.procedure_code} onChange={(v: string) => setFormData({ ...formData, procedure_code: v })} placeholder="CPT/HCPCS" />
                                <InputGroup label="Provider NPI" value={formData.requesting_provider_npi} onChange={(v: string) => setFormData({ ...formData, requesting_provider_npi: v })} placeholder="10 Digits" />
                            </div>
                            <InputGroup label="Diagnosis Codes" value={formData.diagnosis_codes} onChange={(v: string) => setFormData({ ...formData, diagnosis_codes: v })} placeholder="ICD-10 (comma separated)" />

                            <div>
                                <label className="block text-[10px] uppercase font-bold text-neutral-500 mb-1 ml-1">Payer</label>
                                <select
                                    className="w-full bg-neutral-950 border border-neutral-800 rounded-lg px-4 py-2.5 text-sm text-white focus:border-blue-500 outline-none transition-colors"
                                    value={formData.payer_name}
                                    onChange={(e) => setFormData({ ...formData, payer_name: e.target.value })}
                                >
                                    {PAYERS.map(p => <option key={p} value={p}>{p}</option>)}
                                </select>
                            </div>
                            <div>
                                <label className="block text-[10px] uppercase font-bold text-neutral-500 mb-1 ml-1">Urgency</label>
                                <div className="flex gap-4 p-1 bg-neutral-950 border border-neutral-800 rounded-lg">
                                    {['standard', 'urgent'].map(u => (
                                        <button
                                            key={u}
                                            type="button"
                                            onClick={() => setFormData({ ...formData, urgency: u })}
                                            className={cn(
                                                "flex-1 py-1.5 text-xs font-bold rounded-md transition-all capitalize",
                                                formData.urgency === u ? "bg-neutral-800 text-white" : "text-neutral-500 hover:text-neutral-300"
                                            )}
                                        >
                                            {u}
                                        </button>
                                    ))}
                                </div>
                            </div>
                        </div>
                    </div>

                    {/* Clinical Justification */}
                    <div className="bg-neutral-900/50 border border-neutral-800 rounded-2xl overflow-hidden md:col-span-2">
                        <div className="flex border-b border-neutral-800">
                            <TabButton active={activeTab === 'manual'} onClick={() => setActiveTab('manual')} icon={<Keyboard className="size-4" />} label="Manual Notes" />
                            <TabButton active={activeTab === 'ocr'} onClick={() => setActiveTab('ocr')} icon={<Upload className="size-4" />} label="OCR Extract" />
                            <TabButton active={activeTab === 'voice'} onClick={() => setActiveTab('voice')} icon={<Mic className="size-4" />} label="Voice Transcription" />
                        </div>

                        <div className="p-6">
                            <textarea
                                className="w-full bg-neutral-950 border border-neutral-800 rounded-xl p-4 text-sm text-neutral-300 h-48 focus:border-blue-500 outline-none transition-colors overflow-y-auto"
                                placeholder="Enter clinical justification, exam findings, or therapy history..."
                                value={formData.clinical_notes}
                                onChange={(e) => setFormData({ ...formData, clinical_notes: e.target.value })}
                            />
                        </div>
                    </div>
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    className="w-full flex items-center justify-center gap-3 py-4 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-bold rounded-2xl shadow-xl shadow-blue-900/20 transition-all hover:scale-[1.01] active:scale-95"
                >
                    {loading ? <Loader2 className="animate-spin size-5" /> : <Send className="size-5" />}
                    {loading ? "Initializing Swarm..." : "Submit Authorization Request"}
                </button>
            </form>
        </div>
    );
}

function InputGroup({ label, value, onChange, placeholder }: any) {
    return (
        <div>
            <label className="block text-[10px] uppercase font-bold text-neutral-500 mb-1 ml-1">{label}</label>
            <input
                type="text"
                className="w-full bg-neutral-950 border border-neutral-800 rounded-lg px-4 py-2.5 text-sm text-white focus:border-blue-500 outline-none transition-colors"
                placeholder={placeholder}
                value={value}
                onChange={(e) => onChange(e.target.value)}
            />
        </div>
    );
}

function TabButton({ active, onClick, icon, label }: any) {
    return (
        <button
            type="button"
            onClick={onClick}
            className={cn(
                "flex-1 flex items-center justify-center gap-2 py-3 text-xs font-bold transition-all border-b-2",
                active ? "bg-neutral-800/20 border-blue-500 text-blue-400" : "border-transparent text-neutral-500 hover:text-neutral-300"
            )}
        >
            {icon}
            {label}
        </button>
    );
}
