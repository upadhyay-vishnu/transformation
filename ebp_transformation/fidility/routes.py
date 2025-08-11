import os
import zipfile
from pathlib import Path
from typing import Dict, Type

from .annual_load_balance_by_plan import AnnualLoanBalanceByPlan
from .audit_contribution_summary import ParticipantContributionPivotReport
from .audit_rollover_report import AuditRolloverReport
from .balance_by_fund import BalanceByFund
from .balance_info_summary_report_ytd import BalanceInfoSummaryReportYtd
from .base import BaseTransformer, NoTransformer
from .contribution_plan_level_report import ContributionPlanLevelReport
from .loan_withdrawl_report import LoanWithdrawlReport
from .summary_of_net_trust_assets import SummaryOfNetTrustAssets
from .r25_transformation import AuditR25CheckRegister


TRANSFORMER_MAP: Dict[str, Type[BaseTransformer]] = {
    "Annual Loan Balance by Plan": AnnualLoanBalanceByPlan,
    "Balances by Fund": BalanceByFund,
    "Summary of Net Trust Aassets": SummaryOfNetTrustAssets,
    "Contribution Plan Level Report": ContributionPlanLevelReport,
    "Loan Withdrawals Report": LoanWithdrawlReport,
    "Withdrawals Report": LoanWithdrawlReport,
    "Balance Info Summary Report_YE": BalanceInfoSummaryReportYtd,
    "Audit Contribution Summary": ParticipantContributionPivotReport,
    "Audit Rollover Report": AuditRolloverReport,
    "Audit Deferral Elections for a date range":  NoTransformer,
    "Audit R25 Check Register": AuditR25CheckRegister
}

CONSTANT_BASE_PATH = os.path.dirname(os.path.dirname(__file__))
RAW_DATA_DIR_PATH = os.path.join(CONSTANT_BASE_PATH, "data", "raw")
TRANSFORMED_DATA_DIR_PATH = os.path.join(CONSTANT_BASE_PATH, "data", "transformed")

os.makedirs(RAW_DATA_DIR_PATH, exist_ok=True)
os.makedirs(TRANSFORMED_DATA_DIR_PATH, exist_ok=True)


def process_directory(engagement: str):
    input_dir = os.path.join(RAW_DATA_DIR_PATH, engagement)
    output_dir = os.path.join(TRANSFORMED_DATA_DIR_PATH, engagement)

    if not os.path.exists(input_dir):
        return {"error": f"Input directory does not exist: {input_dir}"}

    os.makedirs(output_dir, exist_ok=True)

    for file_name in os.listdir(input_dir):
        file_base = Path(file_name).stem.strip()
        input_file = os.path.join(input_dir, file_name)
        output_file = os.path.join(output_dir, file_name)

        transformer_cls = TRANSFORMER_MAP.get(file_base)
        if transformer_cls:
            transformer = transformer_cls(input_path=input_file, output_path=output_file)
            transformer.transform()
        else:
            print(f"No transformer found for {file_base}")

    return {"status": "processing complete", "engagement": engagement}
