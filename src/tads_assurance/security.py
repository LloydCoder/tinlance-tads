"""M14 security/privacy policy contracts."""

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class SecurityPolicy:
    tenant_context_required: bool = True
    external_content_untrusted: bool = True
    model_output_untrusted: bool = True
    network_egress_restricted: bool = True
    secrets_redacted: bool = True
    personal_data_minimized: bool = True
    audit_required: bool = True

    def validate(self) -> None:
        controls = (
            self.tenant_context_required,
            self.external_content_untrusted,
            self.model_output_untrusted,
            self.network_egress_restricted,
            self.secrets_redacted,
            self.personal_data_minimized,
            self.audit_required,
        )
        if not all(controls):
            raise ValueError("all mandatory TADS security controls must be enabled")


@dataclass(frozen=True, slots=True)
class PrivacyPolicy:
    personal_data_allowed: bool = False
    retention_days: int = 365
    deletion_requires_audit: bool = True
    sensitive_data_requires_explicit_purpose: bool = True

    def validate(self) -> None:
        if self.retention_days <= 0:
            raise ValueError("retention_days must be positive")
        if not self.deletion_requires_audit:
            raise ValueError("privacy deletion must remain auditable")
        if not self.sensitive_data_requires_explicit_purpose:
            raise ValueError("sensitive-data purpose checks are mandatory")
