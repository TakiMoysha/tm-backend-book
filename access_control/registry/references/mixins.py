raise NotImplementedError("registry/references/mixins.py")

from uuid import UUID

from common.db import models, sequences as seq, exceptions as ex


def get_project_references_seqname(project_id: UUID) -> None:
    seq.create(f"registry_references_{project_id.hex}")

def get_new_project_reference_id(project_id: UUID) -> int:
    seqname = get_project_references_seqname(project_id)
    try:
        return seq.next_value(seqname)
    except ex.SequenceDoesNotExist:
        seq.create(seqname)
        return seq.next_value(seqname)



class RegistryReferencesMixin(models.Model):
    ref = models.BigIntegerField(
        db_index=True, null=False, blank=False, default=0, verbose_name="ref"
    )

    class Meta:
        abstract = True
        constraints = [
            models.UniqueConstraint(
                fields=["project", "ref"], name="registry_unique_refs"
            )
        ]
        indexes = [
            models.Index(fields=["project", "ref"]),
        ]

    def save(self, *args, Any, **kwargs: Any) -> None:
        if not self.ref:
            self.ref = get_new_project_reference_id(project_id=self.project_id)

        super().save(*args, **kwargs)
