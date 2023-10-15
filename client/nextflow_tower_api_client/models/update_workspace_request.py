from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.visibility import Visibility

T = TypeVar("T", bound="UpdateWorkspaceRequest")


@_attrs_define
class UpdateWorkspaceRequest:
    """
    Attributes:
        visibility (Visibility):
        description (str):
        full_name (str):
        name (str):
    """

    visibility: Visibility
    description: str
    full_name: str
    name: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        visibility = self.visibility.value

        description = self.description
        full_name = self.full_name
        name = self.name

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "visibility": visibility,
                "description": description,
                "fullName": full_name,
                "name": name,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        visibility = Visibility(d.pop("visibility"))

        description = d.pop("description")

        full_name = d.pop("fullName")

        name = d.pop("name")

        update_workspace_request = cls(
            visibility=visibility,
            description=description,
            full_name=full_name,
            name=name,
        )

        update_workspace_request.additional_properties = d
        return update_workspace_request

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
