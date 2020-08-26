"""Library to interface with Solana public keys."""
from __future__ import annotations

from typing import Any, List, Optional, Tuple, Union

import base58


class PublicKey:
    """The public key of a keypair.

    >>> # An arbitary public key:
    >>> pubkey = PublicKey(1)
    >>> str(pubkey) # String representation in base58 form.
    '11111111111111111111111111111112'
    >>> bytes(pubkey).hex()
    '0000000000000000000000000000000000000000000000000000000000000001'
    """

    LENGTH = 32
    """Constant for standard length of a public key."""

    def __init__(self, value: Union[bytearray, bytes, int, str]) -> None:
        """Init PublicKey object."""
        self._key: Optional[bytes] = None
        if isinstance(value, str):
            self._key = base58.b58decode(value)
            if len(self._key) != self.LENGTH:
                raise ValueError("invalid public key input:", value)
        elif isinstance(value, int):
            self._key = bytes([value])
        else:
            self._key = bytes(value)

        if len(self._key) > self.LENGTH:
            raise ValueError("invalid public key input:", value)

    def __bytes__(self) -> bytes:
        """Public key in bytes."""
        if not self._key:
            return bytes(self.LENGTH)
        return self._key if len(self._key) == self.LENGTH else self._key.rjust(self.LENGTH, b"\0")

    def __eq__(self, other: Any) -> bool:
        """Equality definition for PublicKeys."""
        return False if not isinstance(other, PublicKey) else bytes(self) == bytes(other)

    def __repr__(self) -> str:
        """Representation of a PublicKey."""
        return str(self)

    def __str__(self) -> str:
        """String definition for PublicKey."""
        return self.to_base58().decode("utf-8")

    def to_base58(self) -> bytes:
        """Public key in base58."""
        return base58.b58encode(bytes(self))

    def create_with_seed(self, from_public_key: PublicKey, seed: str, program_id: PublicKey) -> PublicKey:
        """Derive a public key from another key, a seed, and a program ID."""
        raise NotImplementedError("create_with_seed not implemented")

    def create_program_address(self, seeds: Union[bytearray, List[bytes]], program_id: PublicKey) -> PublicKey:
        """Derive a program address from seeds and a program ID."""
        raise NotImplementedError("create_program_address not implemented")

    def find_program_address(
        self, seeds: Union[bytearray, List[bytes]], program_id: PublicKey
    ) -> Tuple[PublicKey, int]:
        """Find a valid program address.

        Valid program addresses must fall off the ed25519 curve.  This function
        iterates a nonce until it finds one that when combined with the seeds
        results in a valid program address.
        """
        raise NotImplementedError("find_program_address not implemented")
