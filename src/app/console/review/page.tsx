import DashboardLayout from "@/components/dashboard/DashboardLayout";
import { DecisionPackage } from "@/components/dashboard/DecisionPackage";
import { Suspense } from "react";

export default function ReviewPage() {
    return (
        <DashboardLayout>
            <Suspense fallback={<div>Loading decision package...</div>}>
                <DecisionPackage />
            </Suspense>
        </DashboardLayout>
    );
}
