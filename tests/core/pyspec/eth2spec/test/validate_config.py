from eth2spec.phase0 import spec as spec_phase0


def validate_minimums(spec):
    minimum_vars = [
        # Misc
        (spec.ETH1_FOLLOW_DISTANCE, 0),  # Would be maximally unsafe in confirming eth1 blocks
        (spec.MAX_COMMITTEES_PER_SLOT, 1),  # 0 technically works because of `get_committee_count_at_slot` ensuring at least 1 but 0 becomes semantically incorrect
        (spec.TARGET_COMMITTEE_SIZE, 1),
        (spec.MAX_VALIDATORS_PER_COMMITTEE, 1),  # This clearly needs to be non-zero but the def is really related to ETH supply
        (spec.MIN_PER_EPOCH_CHURN_LIMIT, 1),  # Otherwise can get into state where no new vals can join
        (spec.CHURN_LIMIT_QUOTIENT, 1),  # Otherwise div by zero
        (spec.SHUFFLE_ROUND_COUNT, 0),  # Shuffle becomes no-op at 0
        (spec.MIN_GENESIS_ACTIVE_VALIDATOR_COUNT, 1),  # Chain cannot handle 0 validators because no blocks can be built
        (spec.MIN_GENESIS_TIME, 0),  # Would start WAY in the past
        (spec.HYSTERESIS_QUOTIENT, 1),  # Avoid div by zero
        (spec.HYSTERESIS_DOWNWARD_MULTIPLIER, 0),
        (spec.HYSTERESIS_UPWARD_MULTIPLIER, 0),

        # Gwei
        (spec.MIN_DEPOSIT_AMOUNT, 0),  # Allows for creation of val-slots for free -- DANGEROUS
        (spec.MAX_EFFECTIVE_BALANCE, 1),  # If all effective balances were 0, would cause div by zero in `get_base_reward`
        (spec.EJECTION_BALANCE, 0),
        (spec.EFFECTIVE_BALANCE_INCREMENT, 1),  # Avoid div by zero in uint overflow avoidance calculations

        # Time
        (spec.MIN_GENESIS_DELAY, 1),  # Avoid modulo by zero in genesis time calculation
        (spec.SECONDS_PER_SLOT, 0),  # All slots happen simultaneously. Non-sensical but maybe valid
        (spec.SECONDS_PER_ETH1_BLOCK, 0),  # 0 doesn't reflect reality and eliminates any follow distance security
        (spec.MIN_ATTESTATION_INCLUSION_DELAY, 1),  # Cannot include attestations from current or future slots
        (spec.SLOTS_PER_EPOCH, 1),  # Should probably ensure that at least 1 attestation from each committe can come in via a more complex relationsh
        (spec.MIN_SEED_LOOKAHEAD, 0),  # Can technically be 0 and take the result of the immediate preceeding epoch. This would cause subnets to fail so maybe should be 1
        (spec.MAX_SEED_LOOKAHEAD, 0),  # Think this can be equal to `MIN_SEED_LOOKAHEAD` but not less
        (spec.MIN_EPOCHS_TO_INACTIVITY_PENALTY, 0),  # Zero means anything except always optimally finalizing previous epoch during current epoch
        (spec.EPOCHS_PER_ETH1_VOTING_PERIOD, 1),
        (spec.SLOTS_PER_HISTORICAL_ROOT, 2 * spec.SLOTS_PER_EPOCH),  # Must be multiple of SLOTS_PER_EPOCH to do the batch accum correctly. Think min two epochs
        (spec.MIN_VALIDATOR_WITHDRAWABILITY_DELAY, 0),  # Don't think this technically needs to be non-zero
        (spec.SHARD_COMMITTEE_PERIOD, 1),  # This _might_ need to be greater than one. Definitely needs to be non-zero in phase 1

        # State list lengths
        (spec.EPOCHS_PER_HISTORICAL_VECTOR, spec.MIN_SEED_LOOKAHEAD + 1),  # Ensure get_seed does not wrap around
        (spec.EPOCHS_PER_SLASHINGS_VECTOR, 1),
        (spec.HISTORICAL_ROOTS_LIMIT, 1),  # Chain breaks after this many epochs
        (spec.VALIDATOR_REGISTRY_LIMIT, 1),  # Chain breaks if more than this many validator records

        # Rewards and penalties
        (spec.BASE_REWARD_FACTOR, 0),  # 0 disables rewards and will break assumptions in tests
        (spec.WHISTLEBLOWER_REWARD_QUOTIENT, 1),
        (spec.PROPOSER_REWARD_QUOTIENT, 1),
        (spec.INACTIVITY_PENALTY_QUOTIENT, 1),
        (spec.MIN_SLASHING_PENALTY_QUOTIENT, 1),  # Should be less than whistleblower quotient to ensure not profitable to slash onesself

        # Max operations
        (spec.MAX_PROPOSER_SLASHINGS, 0),
        (spec.MAX_ATTESTER_SLASHINGS, 0),
        (spec.MAX_ATTESTATIONS, 0),
        (spec.MAX_DEPOSITS, 0),
        (spec.MAX_VOLUNTARY_EXITS, 0),
    ]

    for var, minimum in minimum_vars:
        assert var >= minimum


def validate_gwei_relationships(spec):
    # there must be a valid range for deposit amounts
    assert spec.MAX_EFFECTIVE_BALANCE >= spec.MIN_DEPOSIT_AMOUNT


def validate_randomness(spec):
    pass
    # assert spec.ACTIVATION_EXIT_DELAY >= spec.MIN_SEED_LOOKAHEAD

    # assert spec.LATEST_RANDAO_MIXES_LENGTH > spec.MIN_SEED_LOOKAHEAD
    # must have at least 2 mixes around for the previous and current epoch
    # assert spec.LATEST_RANDAO_MIXES_LENGTH >= 2

def validate_state_lists_relationships(spec):
    pass


def validate_config(spec):
    print("validating constants")
    validate_minimums(spec)
    validate_gwei_relationships(spec)
    validate_randomness(spec)

    # assert spec.LATEST_ACTIVE_INDEX_ROOTS_LENGTH >= spec.ACTIVATION_EXIT_DELAY

    # because slashed balance is calculated halfway between slashed epoch and `LATEST_SLASHED_EXIT_LENGTH` epochs
    # assert spec.LATEST_SLASHED_EXIT_LENGTH >= 2
    print("done validating constants")


if __name__ == '__main__':
    validate_config(spec_phase0)